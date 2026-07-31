import axios from "axios";

const API_BASE = "https://backend.lemonsmoke-b9d4da5c.eastus.azurecontainerapps.io";

export async function login(email, password) {
  const response = await axios.post(`${API_BASE}/auth/login`, { email, password });
  return response.data;
}

export async function sendChatMessage(message, sessionId, token) {
  const response = await axios.post(
    `${API_BASE}/chat`,
    { message, session_id: sessionId },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
}

export async function uploadDocument(file, token) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await axios.post(`${API_BASE}/upload`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`
    },
  });
  return response.data;
}