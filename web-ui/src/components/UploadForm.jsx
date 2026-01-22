import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { api } from "../api";

export default function UploadForm({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      setStatus("Uploading...");

      const res = await api.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (evt) => {
          if (evt.total) {
            const pct = Math.round((evt.loaded / evt.total) * 100);
            setProgress(pct);
          }
        },
      });

      setStatus(res.data.message || "Upload complete!");

      // ✅ Notify App.jsx of new file upload
      if (onUploadSuccess) {
        onUploadSuccess(file.name);
      }

      // Optional: Reset file input
      setFile(null);
    } catch (err) {
      console.error("❌ Upload Error:", err.response?.data || err.message);
      setStatus("Upload failed. Check the console for details.");
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles && acceptedFiles[0]) {
      setFile(acceptedFiles[0]);
      setStatus(`Selected: ${acceptedFiles[0].name}`);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className="bg-gradient-to-br from-indigo-600 to-purple-700 text-white p-8 rounded-3xl shadow-2xl max-w-2xl mx-auto mt-10 text-center transition-all">
      <h1 className="text-4xl font-extrabold mb-6 drop-shadow-lg">📤 Upload a File</h1>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-2xl p-8 mb-6 transition-all ${
          isDragActive ? "bg-indigo-500 border-white" : "bg-indigo-700/20 border-indigo-200"
        }`}
      >
        <input {...getInputProps()} />
        <p className="text-sm">
          Drag & drop a file here, or click to select
        </p>
      </div>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="block w-full text-sm text-white file:mr-4 file:py-2 file:px-6 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-white file:text-indigo-700 hover:file:bg-indigo-100 mb-6 transition-all"
      />

      <button
        onClick={handleUpload}
        disabled={uploading}
        className={`${
          uploading ? "bg-gray-300 cursor-not-allowed" : "bg-white text-indigo-700 hover:bg-indigo-100"
        } font-semibold px-8 py-3 rounded-full shadow-lg transition-all`}
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>

      {progress > 0 && (
        <div className="mt-4 w-full bg-white/20 rounded-full h-2">
          <div
            className="bg-white h-2 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {status && (
        <p className="mt-4 text-sm font-medium text-white bg-black/20 py-2 rounded">
          🔔 {status}
        </p>
      )}
    </div>
  );
}
