from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = PROJECT_ROOT / "backend"


class Settings(BaseSettings):
    APP_NAME: str = "Local RAG"

    APP_VERSION: str = "1.0.0"

    API_PREFIX: str = "/api"

    DEFAULT_LLM: str = "llama3.2:3b"

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    EMBEDDING_DEVICE: str = "cpu"

    CHUNK_SIZE: int = 400

    CHUNK_OVERLAP: int = 150

    UPLOAD_DIRECTORY: Path = BASE_DIR / "storage" / "uploads"

    CHROMA_DIRECTORY: Path = BASE_DIR / "storage" / "chroma_db"

    DEFAULT_MODEL: str = "llama3.2:3b"

    model_config = SettingsConfigDict(
    env_file=PROJECT_ROOT / ".env",
    case_sensitive=True,
    extra="ignore",
)


settings = Settings()

settings.UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
settings.CHROMA_DIRECTORY.mkdir(parents=True, exist_ok=True)