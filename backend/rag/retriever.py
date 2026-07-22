from langchain_core.documents import Document

from backend.rag.vectorstore import VectorStore


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

        return self.vectorstore.similarity_search( # similarity_search is a internal method of VectorStore that performs a similarity search on the vector store and returns the top-k most relevant document chunks based on the provided query.
            collection_name=collection_name,
            query=query,
            k=k,
        )