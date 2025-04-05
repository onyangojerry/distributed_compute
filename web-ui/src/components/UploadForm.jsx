import { useState } from "react";
import axios from "axios";

export default function UploadForm({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [uploading, setUploading] = useState(false);

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

      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
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
    }
  };

  return (
    <div className="bg-gradient-to-br from-indigo-600 to-purple-700 text-white p-10 rounded-3xl shadow-2xl max-w-xl mx-auto mt-20 text-center transition-all">
      <h1 className="text-4xl font-extrabold mb-6 drop-shadow-lg">📤 Upload a File</h1>

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

      {status && (
        <p className="mt-6 text-sm font-medium text-white bg-black bg-opacity-20 py-2 rounded">
          🔔 {status}
        </p>
      )}
    </div>
  );
}
