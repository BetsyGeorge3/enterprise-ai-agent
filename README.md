
# Enterprise AI Knowledge Assistant

## Run with Docker

1. Install Docker Desktop and ensure `docker compose version` succeeds.
2. Copy `.env.example` to `.env` and fill in the Azure, Cosmos DB, SMTP, JWT, and MCP values.
3. From this directory, build and start the stack:

   ```powershell
   docker compose up --build
   ```

4. Open the frontend at `http://localhost:5173`. The backend is exposed at
   `http://localhost:8000` and the internal MCP service at `http://localhost:8080`.

To stop the stack, press `Ctrl+C`; to remove containers, run:

```powershell
docker compose down
```

The backend reaches the MCP service using the Docker network hostname
`mcp-tools`, while the browser reaches the backend through its published host
port. Uploaded documents are persisted in the local `uploaded_files` folder.
=======
# enterprise-ai-agent
Enterprise Multi-Agent AI Platform using LLM, RAG and Agentic AI

