# Distributed File Storage System

A high-availability distributed file storage system with chunking, replication, FastAPI-based backend, and a modern React UI for file uploads and management.

---

## Features

- Chunked file uploads
- Replication across storage nodes
- Node health checking and auto-registration
- Upload/download/delete via REST API
- Sleek React frontend with drag-and-drop and animated feedback
- FastAPI dashboard for debugging/monitoring

---

## Project Structure

```
distributed_storage/
├── controller/               # FastAPI controller node
│   ├── main.py               # Main controller logic
│   ├── templates/           # Jinja2 HTML dashboard
│   └── metadata.json        # Metadata store
├── nodes/                   # Storage nodes (node1, node2, node3)
│   └── main.py              # Stores/retrieves/deletes file chunks
├── utils/                   # Shared utilities
│   └── file_utils.py        # Chunking and assembly functions
├── web-ui/                  # React + Tailwind frontend
│   ├── src/components/      # UploadForm, FileList UI
│   └── App.jsx, main.jsx    # Entry point
├── docker-compose.yml       # Spin up the entire system
└── .env                     # Optional: for secrets like API_KEY
```

---

## How to Run the System

### 1. Clone the repo
```bash
git clone https://github.com/your-username/distributed-storage.git
cd distributed-storage
```

### 2. Start with Docker Compose
Make sure Docker is installed and running.

```bash
docker compose up --build
```

This spins up:
- 1 controller on `localhost:8000`
- 3 storage nodes on ports `9001`, `9002`, `9003`


### 3. Access the dashboard
Visit [http://localhost:8000/dashboard](http://localhost:8000/dashboard) to see registered nodes and uploaded chunks.


### 4. Launch React UI
```bash
cd web-ui
npm install
npm run dev
```
Visit [http://localhost:5173](http://localhost:5173) to open the UI.

---

## API Reference

### File Upload (Backend)
```http
POST /upload
Form: multipart/form-data { file: File }
```

### File Download
```http
GET /download/{filename}
```

### File Delete
```http
DELETE /delete/{filename}
```

---

## Authentication (Optional)
You can enforce API key headers:
```python
headers = { 'x-api-key': 'supersecret' }
```
Set in environment with `API_KEY=supersecret` or pass in Docker Compose.

---

## Testing Checklist
- [x] File chunking and replication works
- [x] Storage nodes auto-register
- [x] Dashboard shows healthy nodes
- [x] Upload via React form
- [x] Files downloadable and deletable

---

## Tech Stack
- **Backend**: FastAPI + Python
- **Frontend**: React + Tailwind + Vite
- **DevOps**: Docker + Docker Compose
- **Styling**: TailwindCSS + Framer Motion

---

## TODO (next features)
- Retry replication on failure
- Node capacity awareness
- File previews (images/docs)
- Auth-based user upload scopes
- Persistent volumes in Docker

---

## 🙌 Author
Jerry "Onyi" Onyango  
Junior @ Pomona College | AI & Distributed Systems Enthusiast

