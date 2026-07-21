from pathlib import Path

from backend.rag.loader import DocumentLoader
from backend.rag.splitter import DocumentSplitter
from backend.rag.vectorstore import VectorStore


class DocumentService:
    """
    Handles document indexing.
    """

    def __init__(self):
        self.loader = DocumentLoader()
        self.splitter = DocumentSplitter()
        self.vectorstore = VectorStore()

    def index_document(
        self,
        file_path: Path,
        collection_name: str,
    ) -> None:
        """
        Load, split, and index a document into ChromaDB.
        """

        documents = self.loader.load(file_path)

        chunks = self.splitter.split(documents)

        self.vectorstore.add_documents(
            collection_name=collection_name,
            documents=chunks,
        )