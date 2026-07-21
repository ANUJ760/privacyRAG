from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from backend.config.settings import settings
from backend.rag.embeddings import get_embedding_model


class VectorStore:

    def __init__(self):
        self.embedding_model = get_embedding_model()

    def __get_collection(self, collection_name: str) -> Chroma:
        return Chroma(
            collection_name=collection_name,
            persist_directory=str(settings.CHROMA_DIRECTORY),
            embedding_function=self.embedding_model,
        )

    def add_documents(self, collection_name: str, documents: list[Document]) -> None:
        if not collection_name.strip():
            raise ValueError("Collection name must be provided.")

        vectorstore = self.__get_collection(collection_name)

        vectorstore.add_documents(documents) # add_documents is a method of Chroma vectorstore that adds the documents to the collection.

    def similarity_search(
        self,
        collection_name: str,
        query: str,
        k: int = 4,
    ) -> list[Document]:

        vectorstore = self.get_collection(collection_name)

        return vectorstore.similarity_search( # similarity_search is a method of Chroma vectorstore that retrieves the top k most similar documents to the query.
            query=query,
            k=k,
        )
