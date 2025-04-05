// src/components/FileList.jsx
import { useEffect, useState } from "react";
import axios from "axios";
import { FiDownload, FiTrash2, FiEye } from "react-icons/fi";

export default function FileList() {
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState(null);

  const fetchFiles = async () => {
    try {
      const res = await axios.get("http://localhost:8000/files");
      setFiles(res.data.files || []);
    } catch (err) {
      console.error("❌ Failed to load files:", err);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleDelete = async (filename) => {
    try {
      await axios.delete(`http://localhost:8000/delete/${filename}`);
      setFiles(files.filter((f) => f !== filename));
    } catch (err) {
      console.error("❌ Delete failed:", err);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto bg-white rounded-xl shadow-md mt-10">
      <h2 className="text-2xl font-bold text-indigo-700 mb-4">📁 Uploaded Files</h2>
      {files.length === 0 ? (
        <p className="text-gray-500">No files available yet.</p>
      ) : (
        <ul className="space-y-3">
          {files.map((file, idx) => (
            <li
              key={idx}
              className="flex justify-between items-center bg-gray-100 rounded-lg px-4 py-3 hover:bg-indigo-50 transition cursor-pointer"
              onClick={() => setSelected(selected === file ? null : file)}
            >
              <span className="font-medium text-indigo-800">{file}</span>
              {selected === file && (
                <div className="flex space-x-4">
                  <a
                    href={`http://localhost:8000/download/${file}`}
                    className="text-green-600 hover:text-green-800"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <FiEye size={18} title="Open" />
                  </a>
                  <a
                    href={`http://localhost:8000/download/${file}`}
                    className="text-blue-600 hover:text-blue-800"
                    download
                  >
                    <FiDownload size={18} title="Download" />
                  </a>
                  <button
                    onClick={(e) => {
                      e.stopPropagation(); // prevent row toggle
                      handleDelete(file);
                    }}
                    className="text-red-600 hover:text-red-800"
                  >
                    <FiTrash2 size={18} title="Delete" />
                  </button>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
