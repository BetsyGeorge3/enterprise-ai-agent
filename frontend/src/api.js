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

export async function sendChatMessageStream(message, sessionId, token, onChunk, onDone) {
  const response = await fetch(`${API_BASE}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop();

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const data = JSON.parse(line.slice(6));
      if (data.done) {
        onDone(data);
      } else if (data.chunk) {
        onChunk(data.chunk);
      }
    }
  }
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

export async function sendFeedback(sessionId, messageId, rating, token) {
  await axios.post(
    `${API_BASE}/feedback`,
    { session_id: sessionId, message_id: messageId, rating },
    { headers: { Authorization: `Bearer ${token}` } }
  );
}