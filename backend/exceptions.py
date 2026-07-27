class CollectionNotFoundError(Exception):
    """Raised when the requested Chroma collection does not exist."""


class DocumentNotFoundError(Exception):
    """Raised when no relevant documents are retrieved."""


class LLMServiceError(Exception):
    """Raised when the LLM cannot generate a response."""


class InvalidModelError(Exception):
    """Raised when a requested model is not enabled."""


class VectorStoreError(Exception):
    """Raised when a vector store operation fails."""
