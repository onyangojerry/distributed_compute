from fastapi import FastAPI, UploadFile, File, Depends, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Set, List
import os, json, shutil, random, requests
from fastapi.middleware.cors import CORSMiddleware

from utils.file_utils import split_file, assemble_file

# Templates for dashboard
templates = Jinja2Templates(directory="controller/templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],  # 👈 Include port 3000 for new UI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

METADATA_FILE = "controller/metadata.json"
REPLICATION_FACTOR = 2  # store each chunk on 2 nodes

# API Key for auth (use docker env)
API_KEY = os.getenv("API_KEY", "supersecret")

def verify_token(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Track registered nodes
REGISTERED_NODES: Set[str] = set()

class NodeInfo(BaseModel):
    node_url: str

def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return {}
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)

def save_metadata(data):
    with open(METADATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.get("/dashboard")
def dashboard(request: Request):
    metadata = load_metadata()
    nodes = list(REGISTERED_NODES)
    healthy_nodes = get_healthy_nodes()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "nodes": nodes,
        "healthy_nodes": healthy_nodes,
        "metadata": metadata,
    })

@app.get("/files")
def list_uploaded_files():
    metadata = load_metadata()
    return {"files": list(metadata.keys())}


@app.delete("/delete/{filename}")
def delete_file(filename: str):
    metadata = load_metadata()
    if filename not in metadata:
        return {"error": "File not found in metadata"}

    for entry in metadata[filename]:
        node = entry["node"]
        chunk = entry["chunk"]
        try:
            requests.delete(f"{node}/delete_chunk/{chunk}")
        except Exception as e:
            print(f"Failed to delete {chunk} from {node}: {e}")

    del metadata[filename]
    save_metadata(metadata)
    return {"message": f"{filename} deleted"}




@app.post("/register")
def register_node(info: NodeInfo):
    REGISTERED_NODES.add(info.node_url)
    print(f"[REGISTER] Node registered: {info.node_url}")
    return {"message": "Node registered", "total": len(REGISTERED_NODES)}

@app.get("/nodes")
def list_registered_nodes():
    return {"nodes": list(REGISTERED_NODES)}

def get_healthy_nodes():
    healthy = []
    for node in REGISTERED_NODES:
        try:
            res = requests.get(f"{node}/health", timeout=1)
            if res.status_code == 200:
                healthy.append(node)
        except:
            print(f"[HEALTH] {node} is DOWN.")
    return healthy

def send_chunk_to_node(node_url, chunk_name, chunk_data):
    try:
        res = requests.post(
            f"{node_url}/store_chunk",
            params={"filename": chunk_name},
            files={"file": (chunk_name, chunk_data)}
        )
        return res.status_code == 200
    except Exception as e:
        print(f"Error sending to {node_url}: {e}")
        return False

def get_chunk_from_node(node_url, chunk_name):
    try:
        res = requests.get(f"{node_url}/get_chunk/{chunk_name}")
        if res.status_code == 200:
            return res.content
    except:
        pass
    return None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)): #, token: str = Depends(verify_token)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = split_file(temp_path)
    os.remove(temp_path)

    healthy_nodes = get_healthy_nodes()
    if len(healthy_nodes) < REPLICATION_FACTOR:
        return {
            "error": f"Not enough healthy nodes to replicate. Needed {REPLICATION_FACTOR}, got {len(healthy_nodes)}"
        }

    metadata = load_metadata()
    metadata[file.filename] = []

    for chunk_name, chunk_data in chunks:
        nodes = random.sample(healthy_nodes, REPLICATION_FACTOR)
        for node in nodes:
            success = send_chunk_to_node(node, chunk_name, chunk_data)
            if success:
                metadata[file.filename].append({"chunk": chunk_name, "node": node})
            else:
                print(f"Failed to store {chunk_name} on {node}")

    save_metadata(metadata)
    return {
        "message": f"{file.filename} uploaded and split into {len(chunks)} chunks with replication.",
        "used_nodes": healthy_nodes
    }

@app.get("/download/{filename}")
def download_file(filename: str): #, token: str = Depends(verify_token)):
    metadata = load_metadata()
    if filename not in metadata:
        return {"error": "File not found."}

    chunks_map = {}
    for entry in metadata[filename]:
        chunks_map.setdefault(entry["chunk"], []).append(entry["node"])

    chunks = []
    for chunk_name, node_list in chunks_map.items():
        for node in node_list:
            data = get_chunk_from_node(node, chunk_name)
            if data:
                chunks.append((chunk_name, data))
                break
        else:
            return {"error": f"Chunk {chunk_name} is missing from all replicas."}

    output_path = f"reconstructed_{filename}"
    with open(output_path, "wb") as f:
        f.write(assemble_file(chunks))

    return FileResponse(output_path, filename=filename)
