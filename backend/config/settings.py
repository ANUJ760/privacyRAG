from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = PROJECT_ROOT / "backend"


class Settings(BaseSettings):
    APP_NAME: str = "Local RAG"

    APP_VERSION: str = "1.0.0"

    API_PREFIX: str = "/api"

    MODEL_NAME: str = "llama3.2:1b"

    DEFAULT_LLM: str = "llama3.2:1b"

    AVAILABLE_MODELS: str = ""

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    LOG_LEVEL: str = "info"

    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    EMBEDDING_DEVICE: str = "cpu"

    CHUNK_SIZE: int = 300

    CHUNK_OVERLAP: int = 100

    UPLOAD_DIRECTORY: Path = BASE_DIR / "storage" / "uploads"

    CHROMA_PERSIST_DIRECTORY: Path = BASE_DIR / "storage" / "chroma_db"

    DEFAULT_MODEL: str = "llama3.2:3b"

    @property
    def CHROMA_DIRECTORY(self) -> Path:
        return self.CHROMA_PERSIST_DIRECTORY

    @property
    def MODEL_OPTIONS(self) -> list[str]:
        models = [
            model.strip()
            for model in self.AVAILABLE_MODELS.split(",")
            if model.strip()
        ]

        if self.MODEL_NAME not in models:
            models.insert(0, self.MODEL_NAME)

        return models

    @property
    def CORS_ORIGIN_LIST(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

settings.UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
settings.CHROMA_PERSIST_DIRECTORY.mkdir(parents=True, exist_ok=True)
