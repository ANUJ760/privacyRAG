# PrivacyRAG Frontend

Next.js client for the PrivacyRAG document chat application.

## Setup

```bash
npm install
```

Create `.env.local`:

```text
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

Run locally:

```bash
npm run dev
```

Open `http://localhost:3000`.

## Checks

```bash
npm run lint
npm run build
```

## Docker

The production image is built from the repository root:

```bash
docker build -f frontend/Dockerfile --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000/api -t privacyrag-frontend .
```

## UI Notes

- Compact dark blue/green interface.
- Courier New monospace typography.
- Straight, low-radius controls.
- macOS-style red/yellow/green window dots in the header.
- Model selector populated by the backend deployment config.
