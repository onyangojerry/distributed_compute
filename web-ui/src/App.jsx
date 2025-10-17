// src/App.jsx
import UploadForm from "./components/UploadForm";
import FileList from "./components/FileList";
import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = () => {
    axios.get("http://localhost:8000/files")
      .then(res => setFiles(res.data.files || []))
      .catch(err => console.error("Failed to load files:", err));
  };

  const handleUploadSuccess = (newFile) => {
    setFiles(prev => [...prev, newFile]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-white p-6">
      <h1 className="text-4xl font-extrabold text-center text-indigo-600 mb-10">
        A Distributed and fault-tolerant File Storage
      </h1>
      <UploadForm onUploadSuccess={handleUploadSuccess} />
      <FileList files={files} />
    </div>
  );
}

export default App;

