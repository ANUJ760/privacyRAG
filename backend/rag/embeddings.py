from functools import lru_cache

from langchain_community.embeddings import HuggingFaceEmbeddings

from backend.config.settings import settings


@lru_cache(maxsize=1) # caches the result of the function so that it is only computed once and reused on subsequent calls.
def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={
            "device": settings.EMBEDDING_DEVICE,
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )
