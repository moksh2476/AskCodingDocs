import React, { useState } from "react";
import { askQuestion } from "../api";

export default function DocChat() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await askQuestion(query);
    setAnswer(res.answer || "No answer found.");
    setLoading(false);
  };

  return (
    <div className="bg-white shadow p-6 rounded-2xl">
      <h2 className="text-xl font-semibold mb-4">💬 Ask about your Docs</h2>
      <form onSubmit={handleAsk} className="flex flex-col gap-3">
        <textarea
          rows="3"
          placeholder="Ask a question about your documentation..."
          className="border p-2 rounded"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Ask
        </button>
      </form>
      {loading && <p className="mt-3 text-gray-500">Thinking...</p>}
      {answer && (
        <div className="mt-3 bg-gray-100 p-3 rounded text-gray-800 whitespace-pre-wrap">
          {answer}
        </div>
      )}
    </div>
  );
}
