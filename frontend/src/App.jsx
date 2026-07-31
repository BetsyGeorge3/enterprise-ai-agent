import { useState, useRef, useEffect } from "react";
import { login, sendChatMessageStream, uploadDocument, sendFeedback } from "./api";
import "./App.css";

function App() {
  const [token, setToken] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingState, setLoadingState] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleLogin = async () => {
    try {
      const result = await login(email, password);
      setToken(result.access_token);
      setLoginError("");
    } catch (err) {
      setLoginError("Login failed — check email/password.");
    }
  };

  const detectLoadingState = (message) => {
    const lower = message.toLowerCase();
    if (lower.includes("github") || lower.includes("issue") || lower.includes("pull request")) {
      return "Checking GitHub…";
    }
    if (lower.includes("sql") || lower.includes("sales") || lower.includes("revenue")) {
      return "Querying data…";
    }
    return "Searching documents…";
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setLoading(true);
    setLoadingState(detectLoadingState(currentInput));

    let streamedText = "";
    setMessages((prev) => [...prev, { role: "assistant", content: "", sources: [] }]);

    try {
      await sendChatMessageStream(
        currentInput,
        sessionId,
        token,
        (chunk) => {
          streamedText += chunk;
          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = { role: "assistant", content: streamedText, sources: [] };
            return updated;
          });
        },
        (final) => {
          setSessionId(final.session_id);
          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = {
              role: "assistant",
              content: streamedText,
              sources: final.sources || [],
              messageId: crypto.randomUUID()
            };
            return updated;
          });
        }
      );
    } catch (err) {
      setMessages((prev) => [...prev.slice(0, -1), { role: "assistant", content: "Error: could not reach backend." }]);
    } finally {
      setLoading(false);
      setLoadingState(null);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadStatus(`Uploading ${file.name}...`);
    try {
      const result = await uploadDocument(file, token);
      setUploadStatus(`Indexed ${result.chunks_indexed} chunks from ${result.filename}`);
    } catch (err) {
      setUploadStatus("Upload failed.");
    }
  };

  const handleFeedback = async (messageId, rating) => {
    try {
      await sendFeedback(sessionId, messageId, rating, token);
    } catch (err) {
      console.error("Feedback failed", err);
    }
  };

  if (!token) {
    return (
      <div className="app-container" style={{ justifyContent: "center", alignItems: "center", display: "flex", flexDirection: "column", gap: "10px" }}>
        <h2>Login</h2>
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleLogin}>Log in</button>
        {loginError && <p style={{ color: "red" }}>{loginError}</p>}
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Enterprise AI Knowledge Assistant</h1>
        <div className="upload-box">
          <input type="file" onChange={handleFileUpload} />
          {uploadStatus && <span className="upload-status">{uploadStatus}</span>}
        </div>
      </header>

      <main className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="message-bubble">
              {msg.content}
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">Sources: {msg.sources.join(", ")}</div>
              )}
              {msg.role === "assistant" && msg.messageId && (
                <div className="feedback-buttons">
                  <button onClick={() => handleFeedback(msg.messageId, "up")}>👍</button>
                  <button onClick={() => handleFeedback(msg.messageId, "down")}>👎</button>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-bubble">{loadingState || "Thinking..."}</div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>

      <footer className="chat-input">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask something..."
          rows={2}
        />
        <button onClick={handleSend} disabled={loading}>Send</button>
      </footer>
    </div>
  );
}

export default App;