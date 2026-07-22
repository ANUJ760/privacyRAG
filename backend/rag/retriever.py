from langchain_core import documents
from langchain_core.documents import Document

from backend.rag.vectorstore import VectorStore

from backend.exceptions import (
    DocumentNotFoundError,
    VectorStoreError,
)

class Retriever:
    """
    Retrieves relevant document chunks from the vector store.
    """

    def __init__(self):
        self.vectorstore = VectorStore()

    def retrieve(self, collection_name: str, query: str, k: int = 4,) -> list[Document]:
        """
        Retrieve the top-k most relevant document chunks.
        """

        documents = self.vectorstore.similarity_search(
        collection_name=collection_name,
        query=query,
        k=k,
    )

        if not documents:
            raise DocumentNotFoundError(
                "No relevant documents were found."
            )

        return documents