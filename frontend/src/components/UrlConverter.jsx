import React, { useState } from "react";
import { convertUrl } from "../api";

export default function UrlConverter() {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState("");
  const [docs, setDocs] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("Processing...");
    try {
      const res = await convertUrl(url);
      if (res.success) {
        setStatus(`✅ Saved as ${res.filename}`);
      } else {
        setStatus("❌ Failed to convert URL");
      }
    } catch {
      setStatus("❌ Server error");
    }
  };

  return (
    <div>
    <div className="bg-white shadow p-6 rounded-2xl">
      <h2 className="text-xl font-semibold mb-4">🌐 Convert URL to Text</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          type="url"
          placeholder="Enter a website URL..."
          className="border p-2 rounded"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Convert
        </button>
      </form>
      {status && <p className="mt-3 text-gray-700">{status}</p>}
    </div>

    {/* 📁 Saved Docs Section */}
      <div className="bg-white shadow p-6 rounded-2xl mt-6">
        <h3 className="text-lg font-semibold mb-3">📄 Saved Documents</h3>
        {docs.length === 0 ? (
          <p className="text-gray-500">No documents saved yet.</p>
        ) : (
          <ul style={{ textAlign: "left", paddingLeft: "1rem" }}>
            {docs.map((doc, index) => (
              <li key={index} style={{ marginBottom: "6px" }}>
                {doc}
              </li>
            ))}
          </ul>
        )}
      </div>
      </div>
  );
}