# PrivacyRAG

Local document question-answering application built with FastAPI, LangChain, ChromaDB, Ollama, and Next.js.

## Features

- Upload PDF, DOCX, and TXT documents.
- Extract document text and split it into retrieval chunks.
- Store embeddings in a persistent ChromaDB vector store.
- Ask questions against the uploaded document collection.
- Use recent chat history to resolve follow-up questions.
- Handle summaries, lists, comparisons, extraction requests, timelines, and document-wide overview questions.
- Keep answers grounded in retrieved document context and say when information is missing.
- Use a compact dark blue/green Courier-style interface.

## Tech Stack

Backend:

- FastAPI
- LangChain
- ChromaDB
- Hugging Face sentence-transformer embeddings
- Ollama chat model
- PyMuPDF, docx2txt, TextLoader

Frontend:

- Next.js
- React
- TypeScript
- Axios
- Tailwind CSS
- shadcn-style UI components

## Project Structure

```text
backend/
  api/                 FastAPI route handlers
  config/              Application settings
  llm/                 Ollama model wrapper
  models/              Request and response schemas
  prompts/             System and user prompt builders
  rag/                 Loading, splitting, embeddings, retrieval, vector store
  services/            Chat and document indexing services
  storage/             Uploaded files and ChromaDB persistence

frontend/
  src/app/             Next.js app routes
  src/components/      UI, upload, chat, and layout components
  src/lib/             API client and utilities
  src/providers/       Shared document state
  src/services/        HTTP service functions
  src/types/           TypeScript request/response types
```

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer
- npm
- Ollama
- A local Ollama model matching `DEFAULT_LLM`

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

## Backend Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Pull the default Ollama model:

```bash
ollama pull llama3.2:3b
```

Run the backend:

```bash
uvicorn backend.main:app --reload
```

Default backend URL:

```text
http://localhost:8000
```

## Frontend Setup

Install dependencies:

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```text
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

Run the frontend:

```bash
npm run dev
```

Default frontend URL:

```text
http://localhost:3000
```

## Docker Deployment

This repository includes Docker deployment files for running the frontend and backend on an Azure Ubuntu VM. Ollama is not containerized; install and run Ollama directly on the VM.

Docker files:

- `backend/Dockerfile`
- `backend/.dockerignore`
- `frontend/Dockerfile`
- `frontend/.dockerignore`
- `docker-compose.yml`

Create environment files from the samples:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

For Azure, update the public frontend API URL before building:

```bash
export NEXT_PUBLIC_API_URL=http://<azure-vm-public-ip-or-domain>:8000/api
```

The backend reaches Ollama on the VM host through:

```text
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

Enable user-selectable Ollama models by listing models installed on the VM:

```text
MODEL_NAME=llama3.2:3b
AVAILABLE_MODELS=llama3.2:3b,mistral:7b,qwen2.5:7b
```

`MODEL_NAME` is the default selected model. `AVAILABLE_MODELS` controls the models shown in the deployed UI selector.

`docker-compose.yml` maps `host.docker.internal` to Docker's host gateway so the backend container can call the Ollama process running directly on the Azure VM.

Start the stack:

```bash
docker compose up -d --build
```

Stop the stack:

```bash
docker compose down
```

ChromaDB persistence is stored in the named Docker volume `chroma_data`, mounted at:

```text
/app/backend/storage/chroma_db
```

Uploaded files are stored in the named Docker volume `upload_data`.

Health checks:

- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost:3000`

## CI/CD

GitHub Actions workflow:

```text
.github/workflows/ci-cd.yml
```

The pipeline runs on pull requests and pushes to `main` or `master`:

1. Compile-check the backend.
2. Install frontend dependencies.
3. Run frontend lint.
4. Build the frontend.
5. Build backend and frontend Docker images.

Optional Azure VM deployment runs on pushes to `main` or `master` when this repository variable is set:

```text
ENABLE_AZURE_DEPLOY=true
```

Required GitHub secrets for deployment:

```text
AZURE_VM_HOST       Azure VM public IP or DNS name
AZURE_VM_USER       SSH username
AZURE_VM_SSH_KEY    Private SSH key with access to the VM
```

Optional secret:

```text
AZURE_VM_APP_DIR    App directory on the VM, defaults to ~/privacyRAG
```

The deploy job SSHes into the VM, pulls the latest code, creates `backend/.env` from the example only if missing, rebuilds the Compose stack, starts it in detached mode, and prunes old Docker images.

## API

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

### Upload Document

```http
POST /api/upload/
Content-Type: multipart/form-data
```

Form field:

```text
file
```

Supported extensions:

```text
.pdf, .docx, .txt
```

Response:

```json
{
  "message": "File uploaded successfully.",
  "original_filename": "document.pdf",
  "stored_filename": "generated-name.pdf",
  "path": "backend/storage/uploads/generated-name.pdf",
  "collection_name": "document"
}
```

### List Models

```http
GET /api/chat/models
```

Response:

```json
{
  "default_model": "llama3.2:3b",
  "models": ["llama3.2:3b", "mistral:7b"]
}
```

The frontend uses this endpoint to populate the model selector.

### Ask A Question

```http
POST /api/chat/
Content-Type: application/json
```

Request:

```json
{
  "collection_name": "document",
  "model_name": "llama3.2:3b",
  "question": "What is the file about?",
  "history": [
    {
      "role": "user",
      "content": "Explain the file"
    },
    {
      "role": "assistant",
      "content": "The document describes..."
    }
  ]
}
```

Response:

```json
{
  "answer": "The document is about..."
}
```

## Retrieval Flow

1. Uploaded files are saved under `backend/storage/uploads`.
2. The document loader extracts text based on file extension.
3. The splitter creates overlapping text chunks.
4. Existing Chroma collections with the same generated collection name are cleared.
5. New chunks are embedded and stored in ChromaDB under `backend/storage/chroma_db`.
6. Chat requests retrieve relevant chunks from the selected collection.
7. Broad document questions retrieve a larger ordered slice of the document instead of relying only on similarity search.
8. Retrieved chunks are sent to the LLM with chunk labels and available source/page metadata.
9. The LLM answers using only the retrieved context and clearly reports unsupported or missing details.

## Development Commands

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

Frontend lint:

```bash
cd frontend
npm run lint
```

Frontend production build:

```bash
cd frontend
npm run build
```

## Notes

- Re-upload a document after changing indexing behavior so its Chroma collection is rebuilt.
- The first embedding run may download the configured Hugging Face model.
- The backend CORS configuration allows `http://localhost:3000`.
- Chroma collection names are generated from uploaded filenames by lowercasing and replacing unsupported characters with underscores.
