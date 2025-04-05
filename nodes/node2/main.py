from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import requests
import time

app = FastAPI()

# Environment configs
NODE_PORT = os.getenv("NODE_PORT", "9002")
CONTROLLER_URL = os.getenv("CONTROLLER_URL", "http://localhost:8000")
STORAGE_PATH = "storage/"
os.makedirs(STORAGE_PATH, exist_ok=True)

# Register with the controller on startup
def register_with_controller():
    hostname = os.getenv("HOSTNAME", "node2")
    node_url = f"http://{hostname}:{NODE_PORT}"
    
    for _ in range(5):
        try:
            res = requests.post(
                f"{CONTROLLER_URL}/register",
                json={"node_url": node_url}
            )
            if res.status_code == 200:
                print(f"[AUTO-REGISTER] Registered as {node_url}")
                return
        except Exception as e:
            print(f"[ERROR] Could not register with controller: {e}")
        time.sleep(2)


@app.on_event("startup")
def startup_event():
    register_with_controller()

# Endpoint to store a chunk
@app.post("/store_chunk")
async def store_chunk(filename: str, file: UploadFile = File(...)):
    with open(os.path.join(STORAGE_PATH, filename), "wb") as f:
        f.write(await file.read())
    return {"status": "stored"}

# Endpoint to retrieve a chunk
@app.get("/get_chunk/{filename}")
def get_chunk(filename: str):
    path = os.path.join(STORAGE_PATH, filename)
    if os.path.exists(path):
        return FileResponse(path, filename=filename)
    return {"error": "not found"}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


@app.delete("/delete_chunk/{filename}")
def delete_chunk(filename: str):
    path = os.path.join(STORAGE_PATH, filename)
    if os.path.exists(path):
        os.remove(path)
        return {"status": "deleted"}
    return {"error": "chunk not found"}
