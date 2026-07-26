from pathlib import Path

from backend.rag.loader import DocumentLoader
from backend.rag.splitter import DocumentSplitter
from backend.rag.vectorstore import VectorStore


class DocumentService:
    """
    Handles document indexing.
    """

    def __init__(self):
        """
        Initialize the loader, splitter, and vector store used for indexing.
        """

        self.loader = DocumentLoader()
        self.splitter = DocumentSplitter()
        self.vectorstore = VectorStore()

    def index_document(
        self,
        file_path: Path,
        collection_name: str,
    ) -> None:
        """
        Load a document from disk, split it into chunks, and index it in ChromaDB.

        Args:
            file_path: Path to the saved document that should be indexed.
            collection_name: Chroma collection where the chunks should be stored.
        """

        documents = self.loader.load(file_path)

        chunks = self.splitter.split(documents)

        self.vectorstore.clear_collection(collection_name)

        self.vectorstore.add_documents(
            collection_name=collection_name,
            documents=chunks,
        )
