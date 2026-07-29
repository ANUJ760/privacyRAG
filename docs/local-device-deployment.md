# Local Device Deployment

Use this mode when each user should keep uploaded documents, embeddings, and
LLM prompts on their own computer instead of on a shared Azure VM.

In this setup, the user's machine runs:

- Ollama and the selected local model
- the FastAPI backend
- the Next.js frontend
- local Docker volumes for uploaded files and ChromaDB

The app is bound to `127.0.0.1`, so it is reachable from the user's device only
unless they intentionally change the port bindings.

## Requirements

- Docker Desktop or Docker Engine with Docker Compose
- Ollama
- A local Ollama model matching `MODEL_NAME`

## Setup

Pull the default model:

```bash
ollama pull llama3.2:3b
```

Start Ollama:

```bash
ollama serve
```

Create a local environment file:

```bash
cp .env.local.example .env
```

Start the app:

```bash
docker compose -f docker-compose.local.yml up -d --build
```

Open the frontend:

```text
http://localhost:3000
```

Health check:

```text
http://localhost:8000/health
```

## Stored Data

Uploaded files are stored in the local Docker volume `upload_data`.
ChromaDB data is stored in the local Docker volume `chroma_data`.

To stop the app without deleting local data:

```bash
docker compose -f docker-compose.local.yml down
```

To delete the local uploaded files and vector database:

```bash
docker compose -f docker-compose.local.yml down -v
```

## Privacy Boundary

This mode avoids a shared server-side document store. The user still needs to
trust software running on their own machine, but uploaded documents and retrieved
chunks are not stored on your Azure VM and are not sent to an external LLM API by
this app.

If you distribute this to other users, package these steps in an installer or
desktop wrapper so they do not need to run Docker commands manually.
