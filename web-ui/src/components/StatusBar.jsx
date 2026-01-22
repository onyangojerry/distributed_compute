import { useEffect, useState } from "react";
import { api } from "../api";

export default function StatusBar() {
  const [nodes, setNodes] = useState([]);
  const [filesCount, setFilesCount] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [nRes, fRes] = await Promise.all([
          api.get("/nodes"),
          api.get("/files"),
        ]);
        setNodes(nRes.data.nodes || []);
        setFilesCount((fRes.data.files || []).length);
        setError("");
      } catch (e) {
        setError("Backend unreachable");
      }
    };
    fetchData();
    const id = setInterval(fetchData, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="flex items-center justify-between bg-white rounded-xl shadow p-4 mb-6 border border-gray-100">
      <div className="flex items-center space-x-3">
        <span className={`h-3 w-3 rounded-full ${error ? "bg-red-500" : "bg-emerald-500"}`} />
        <span className="text-sm text-gray-700">
          {error ? error : "Controller online"}
        </span>
      </div>
      <div className="flex items-center space-x-4">
        <span className="text-sm text-gray-700">
          Nodes: <strong>{nodes.length}</strong>
        </span>
        <span className="text-sm text-gray-700">
          Files: <strong>{filesCount}</strong>
        </span>
      </div>
    </div>
  );
}
