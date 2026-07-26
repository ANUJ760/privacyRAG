from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from backend.config.settings import settings
from backend.rag.embeddings import get_embedding_model

from backend.exceptions import VectorStoreError

class VectorStore:

    def __init__(self):
        """
        Initialize the vector store wrapper with the shared embedding model.
        """

        self.embedding_model = get_embedding_model()

    def __get_collection(self, collection_name: str) -> Chroma: # private method to get a Chroma collection handle.
        """
        Create a Chroma collection handle using the configured persistence path.

        Args:
            collection_name: Name of the Chroma collection to access.
        """

        return Chroma(
            collection_name=collection_name,
            persist_directory=str(settings.CHROMA_DIRECTORY),
            embedding_function=self.embedding_model,
        )

    def add_documents(self, collection_name: str, documents: list[Document]) -> None:
        """
        Add document chunks to a named Chroma collection.

        Args:
            collection_name: Chroma collection where documents should be stored.
            documents: LangChain documents to embed and persist.
        """

        if not collection_name.strip():
            raise ValueError("Collection name must be provided.")

        vectorstore = self.__get_collection(collection_name)

        vectorstore.add_documents(documents) # add_documents is a method of Chroma vectorstore that adds the documents to the collection.

    def clear_collection(self, collection_name: str) -> None:
        """
        Remove an existing collection before replacing it with a fresh upload.
        """

        if not collection_name.strip():
            raise ValueError("Collection name must be provided.")

        try:
            vectorstore = self.__get_collection(collection_name)
            vectorstore.delete_collection()

        except Exception:
            # Chroma raises if the collection does not exist yet. That is fine
            # when indexing a file for the first time.
            return

    def similarity_search(
        self,
        collection_name: str,
        query: str,
        k: int = 4,
    ) -> list[Document]:
        """
        Retrieve the most similar documents from a collection for a query.

        Args:
            collection_name: Chroma collection to search.
            query: Natural language search query.
            k: Maximum number of matching documents to return.
        """

        try:
            vectorstore = self.__get_collection(collection_name)

            return vectorstore.similarity_search(
                query=query,
                k=k,
            )

        except Exception as error:
            raise VectorStoreError(str(error)) from error

    def get_documents(
        self,
        collection_name: str,
        limit: int = 12,
    ) -> list[Document]:
        """
        Return stored chunks from a collection for document-level overview queries.

        Chroma returns records in insertion order, which matches the order chunks
        were indexed for newly uploaded documents.
        """

        try:
            vectorstore = self.__get_collection(collection_name)
            results = vectorstore.get(
                limit=limit,
                include=["documents", "metadatas"],
            )

            contents = results.get("documents") or []
            metadatas = results.get("metadatas") or []

            return [
                Document(
                    page_content=content,
                    metadata=metadatas[index] if index < len(metadatas) else {},
                )
                for index, content in enumerate(contents)
                if content
            ]

        except Exception as error:
            raise VectorStoreError(str(error)) from error
