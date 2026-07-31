# PrivacyRAG

PrivacyRAG is a local document question-answering app. Upload PDF, DOCX, or TXT
files, index them into ChromaDB, and ask grounded questions through a Next.js
chat interface backed by FastAPI, LangChain, Hugging Face embeddings, and
Ollama.

The default setup runs on your own machine. Uploaded documents, vector data, and
prompts stay local unless you choose to deploy the app to a server.

## Contents

- [Features](#features)
- [Limitations](#limitations)
- [Privacy and Security](#privacy-and-security)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Run Locally](#run-locally)
- [Configuration](#configuration)
- [Docker](#docker)
- [API](#api)
- [Development Checks](#development-checks)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- Upload PDF, DOCX, and TXT documents.
- Split documents into retrieval chunks and store embeddings in ChromaDB.
- Ask questions across the uploaded document collection.
- Use chat history for follow-up questions.
- Choose from locally installed Ollama models.
- Return answers grounded in retrieved context, with clear gaps when the
  documents do not contain enough information.
- Preserve uploaded files and vector indexes between restarts.
- Run locally without a hosted LLM provider.
- Deploy as a single-user Docker Compose stack when a hosted trial is needed.
- Use a compact chat UI with document upload, model selection, and streaming-like
  answer display.

## Limitations

- Privacy depends on where you run it. A local device keeps files on that
  device; a server deployment stores files and embeddings on that server.
- The app does not include authentication or multi-user access control.
- Uploaded documents are saved to local storage and are not encrypted by the app.
- Retrieval quality depends on chunk size, embedding model, document formatting,
  and the selected Ollama model.
- Answers can still be incomplete or incorrect when retrieval misses relevant
  context or the model misreads the provided chunks.
- Large documents and larger Ollama models need more CPU, memory, and disk
  space.
- The first embedding run may download the configured Hugging Face model.
- Only PDF, DOCX, and TXT uploads are supported.

## Privacy and Security

- Local development stores uploads under `backend/storage/uploads`.
- ChromaDB data is stored under `backend/storage/chroma_db`.
- Docker deployments store uploads and ChromaDB data in the `upload_data` and
  `chroma_data` volumes.
- Ollama prompts are sent to the Ollama server configured by
  `OLLAMA_BASE_URL`.
- Environment files and runtime data are ignored by Git.
- The root `.dockerignore` also keeps local secrets and runtime data out of
  Docker build contexts.

Before making a fork public, check local files for secrets and rotate any real
credentials that were ever saved in `.env` files.

## Tech Stack

- Backend: FastAPI, LangChain, ChromaDB, PyMuPDF, docx2txt, TextLoader
- Models: Ollama chat models and `BAAI/bge-small-en-v1.5` embeddings
- Frontend: Next.js, React, TypeScript, Tailwind CSS, Axios
- Deployment: Docker Compose, optional GitHub Actions workflow

## Project Structure

```text
backend/
  api/          FastAPI routes
  config/       Application settings
  llm/          Ollama client wrapper
  models/       Request and response schemas
  prompts/      Prompt builders
  rag/          Loading, splitting, embeddings, retrieval, vector storage
  services/     Document indexing and chat services
  storage/      Local uploads and ChromaDB data, ignored by Git

frontend/
  src/app/        Next.js app routes
  src/components/ Chat, upload, layout, and UI components
  src/lib/        API client and utilities
  src/providers/  Shared document state
  src/services/   HTTP service functions
  src/types/      TypeScript types

docs/             Deployment guides
scripts/          VM setup helpers
tests/            Backend smoke checks
```

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer
- npm
- Ollama
- An Ollama model installed locally, such as `llama3.2:3b`

Default backend settings:

```text
MODEL_NAME=llama3.2:3b
AVAILABLE_MODELS=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
EMBEDDING_DEVICE=cpu
CHUNK_SIZE=400
CHUNK_OVERLAP=150
```

## Run Locally

Install the Ollama model:

```bash
ollama pull llama3.2:3b
```

Start the backend:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

The backend runs at:

```text
http://localhost:8000
```

Start the frontend in another terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

The frontend runs at:

```text
http://localhost:3000
```

## Configuration

Backend settings are loaded from `.env` at the repository root. Use the example
files as starting points:

```bash
cp .env.local.example .env
```

Common settings:

| Variable | Purpose | Default |
| --- | --- | --- |
| `MODEL_NAME` | Default Ollama chat model | `llama3.2:3b` |
| `AVAILABLE_MODELS` | Comma-separated models shown in the UI | `llama3.2:3b` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:3000,http://127.0.0.1:3000` |
| `EMBEDDING_MODEL` | Hugging Face embedding model | `BAAI/bge-small-en-v1.5` |
| `EMBEDDING_DEVICE` | Embedding runtime device | `cpu` |
| `CHUNK_SIZE` | Text chunk size for indexing | `400` |
| `CHUNK_OVERLAP` | Overlap between chunks | `150` |

Frontend settings live in `frontend/.env.local`:

```text
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Docker

For a local Docker run that binds services to `127.0.0.1`:

```bash
cp .env.local.example .env
docker compose -f docker-compose.local.yml up -d --build
```

For a server deployment, create an environment file from the Azure sample and
set the public API URL before building:

```bash
cp .env.azure-single-tenant.example .env
```

```text
NEXT_PUBLIC_API_URL=http://<vm-public-ip-or-domain>:8000/api
```

Then start the stack:

```bash
docker compose up -d --build
```

Ollama is expected to run directly on the host. The backend container reaches it
through:

```text
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

Uploaded files and ChromaDB data are stored in Docker volumes:

```text
upload_data
chroma_data
```

See [docs/local-device-deployment.md](docs/local-device-deployment.md) and
[docs/azure-one-vm-per-user.md](docs/azure-one-vm-per-user.md) for full
deployment notes.

## API

Health check:

```http
GET /health
```

List available chat models:

```http
GET /api/chat/models
```

Upload a document:

```http
POST /api/upload/
Content-Type: multipart/form-data
```

Ask a question:

```http
POST /api/chat/
Content-Type: application/json
```

Example request:

```json
{
  "collection_name": "document",
  "model_name": "llama3.2:3b",
  "question": "What is the file about?",
  "history": []
}
```

Example response:

```json
{
  "answer": "The document is about..."
}
```

## How Retrieval Works

1. The upload endpoint validates the file extension and saves the document.
2. The loader extracts text from PDF, DOCX, or TXT input.
3. The splitter creates overlapping chunks.
4. Chunks are embedded and written to a ChromaDB collection.
5. Chat requests retrieve relevant chunks from the selected collection.
6. Broad overview questions can retrieve a larger ordered slice of the document.
7. The selected Ollama model answers using the retrieved context.

## Development Checks

Backend syntax check:

```bash
python -m compileall backend
```

Backend smoke checks:

```bash
python tests/loader_test.py
python tests/splitter_test.py
python tests/vectorstore_test.py
python tests/retriever_test.py
python tests/llm_test.py
```

Frontend checks:

```bash
cd frontend
npm run lint
npm run build
```

## CI/CD

The GitHub Actions workflow in `.github/workflows/ci-cd.yml` runs backend syntax
checks, frontend linting, frontend builds, and Docker image builds on pull
requests and pushes to `main` or `master`.

Optional Azure VM deployment runs only when this repository variable is set:

```text
ENABLE_AZURE_DEPLOY=true
```

Deployment uses these GitHub secrets:

```text
AZURE_VM_HOST
AZURE_VM_USER
AZURE_VM_SSH_KEY
```

Optional:

```text
AZURE_VM_APP_DIR
```

## Troubleshooting

- `Connection refused` from the backend usually means Ollama is not running or
  `OLLAMA_BASE_URL` points to the wrong host.
- Empty or weak answers usually mean no document was uploaded, the wrong
  collection was selected, or the document needs to be re-uploaded after an
  indexing change.
- Slow uploads or answers are usually caused by large documents, CPU-only
  embeddings, or a larger Ollama model.
- If the frontend cannot reach the backend, check `NEXT_PUBLIC_API_URL` and
  `CORS_ORIGINS`.
- If Docker cannot reach Ollama, confirm Ollama is running on the host and that
  `OLLAMA_BASE_URL=http://host.docker.internal:11434` is set for the container.

## Public Repository Notes

- Local environment files, uploaded documents, ChromaDB data, Python virtual
  environments, Node dependencies, and build output are ignored by Git.
- Do not commit `.env`, `frontend/.env.local`, `backend/storage/`, `.venv/`,
  `frontend/node_modules/`, or `frontend/.next/`.
- If real credentials were ever placed in local env files, rotate them before
  publishing the repository.

