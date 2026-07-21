from langchain_community.embeddings import HuggingFaceEmbeddings

from backend.config.settings import settings


class EmbeddingModel:

    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    def get_model(self) -> HuggingFaceEmbeddings:
        return self.embedding_model
