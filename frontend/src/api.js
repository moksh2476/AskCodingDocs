const API_BASE = "http://localhost:8000"; // Your FastAPI backend URL

export async function convertUrl(url) {
  const response = await fetch(`${API_BASE}/convert-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  return response.json();
}

export async function askQuestion(query) {
  const response = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  return response.json();
}

export async function listDocs() {
  const response = await fetch("http://localhost:8000/list-docs");
  return response.json();
}
