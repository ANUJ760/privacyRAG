#!/usr/bin/env bash
set -euo pipefail

if [ -z "${REPO_URL:-}" ]; then
  echo "Set REPO_URL to your PrivacyRAG git repository URL."
  echo "Example: REPO_URL=https://github.com/you/privacyRAG.git PUBLIC_HOST=1.2.3.4 bash scripts/setup-azure-single-tenant-vm.sh"
  exit 1
fi

if [ -z "${PUBLIC_HOST:-}" ]; then
  echo "Set PUBLIC_HOST to the VM public IP address or DNS name."
  exit 1
fi

APP_DIR="${APP_DIR:-$HOME/privacyRAG}"
MODEL_NAME="${MODEL_NAME:-llama3.2:3b}"
AVAILABLE_MODELS="${AVAILABLE_MODELS:-$MODEL_NAME}"

sudo apt-get update
sudo apt-get install -y ca-certificates curl git docker.io docker-compose-plugin

sudo systemctl enable --now docker
sudo usermod -aG docker "$USER" || true

if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

sudo systemctl enable --now ollama
ollama pull "$MODEL_NAME"

if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull --ff-only
else
  git clone "$REPO_URL" "$APP_DIR"
fi

cat > "$APP_DIR/.env" <<ENV
NEXT_PUBLIC_API_URL=http://$PUBLIC_HOST:8000/api
OLLAMA_BASE_URL=http://host.docker.internal:11434
MODEL_NAME=$MODEL_NAME
AVAILABLE_MODELS=$AVAILABLE_MODELS
CORS_ORIGINS=http://$PUBLIC_HOST:3000,http://localhost:3000,http://127.0.0.1:3000
LOG_LEVEL=info
ENV

cd "$APP_DIR"
sudo docker compose up -d --build

echo "PrivacyRAG is starting."
echo "Frontend: http://$PUBLIC_HOST:3000"
echo "Backend health: http://$PUBLIC_HOST:8000/health"
