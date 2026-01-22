// src/App.jsx
import UploadForm from "./components/UploadForm";
import FileList from "./components/FileList";
import StatusBar from "./components/StatusBar";
import { useEffect, useState } from "react";
import { api } from "./api";

function App() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    fetchFiles();
  }, []);

  const [error, setError] = useState("");

  const fetchFiles = () => {
    api.get("/files")
      .then(res => {
        setFiles(res.data.files || []);
        setError("");
      })
      .catch(err => {
        setError("Cannot reach backend. Is the controller running?");
        console.error("Failed to load files:", err);
      });
  };

  const handleUploadSuccess = (newFile) => {
    setFiles(prev => [...prev, newFile]);
  };

  const handleFileDeleted = (deletedFile) => {
    setFiles(prev => prev.filter(file => file !== deletedFile));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-white p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-extrabold text-center text-indigo-600 mb-6">
          Distributed & Fault-Tolerant File Storage
        </h1>
        <StatusBar />
        {error && (
          <div className="mb-6 rounded-lg bg-red-50 border border-red-200 text-red-700 p-4 text-sm">
            {error}
          </div>
        )}
        <UploadForm onUploadSuccess={handleUploadSuccess} />
        <FileList files={files} onFileDeleted={handleFileDeleted} />
      </div>
    </div>
  );
}

export default App;

