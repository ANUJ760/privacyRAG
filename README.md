# PrivacyRAG

Local document question-answering application built with FastAPI, LangChain, ChromaDB, Ollama, and Next.js.

## Features

- Upload PDF, DOCX, and TXT documents.
- Extract document text and split it into retrieval chunks.
- Store embeddings in a persistent ChromaDB vector store.
- Ask questions against the uploaded document collection.
- Use recent chat history to resolve follow-up questions.
- Handle broad document overview questions such as "what is the file about" and "summarize this document".

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
DEFAULT_LLM=llama3.2:3b
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

### Chat

```http
POST /api/chat/
Content-Type: application/json
```

Request:

```json
{
  "collection_name": "document",
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
7. Broad overview questions retrieve document chunks directly instead of relying only on similarity search.
8. The LLM answers using only the retrieved context.

## Development Commands

Backend syntax check:

```bash
python -m compileall backend
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
