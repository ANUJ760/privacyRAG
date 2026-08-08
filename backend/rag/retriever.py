import numpy as np
from langchain_core.documents import Document

from backend.rag.embeddings import get_embedding_model
from backend.rag.vectorstore import VectorStore

from backend.exceptions import DocumentNotFoundError


OVERVIEW_EXAMPLES = (
    "what is the file about",
    "what is this file about",
    "what is the document about",
    "what is this document about",
    "tell me about the file",
    "tell me about this file",
    "explain the document",
    "explain this document",
    "what is inside",
    "what does it contain",
    "summarize",
    "summary",
    "overview",
    "give me the gist",
    "walk me through this document",
    "what's this document about in short",
)

OVERVIEW_SIMILARITY_THRESHOLD = 0.75


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr = np.array(a)
    b_arr = np.array(b)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if denom == 0:
        return 0.0
    return float(np.dot(a_arr, b_arr) / denom)


class Retriever:
    """
    Retrieves relevant document chunks from the vector store.
    """

    def __init__(self):
        self.vectorstore = VectorStore()
        # Computed lazily on first use, then cached for the lifetime of this
        # Retriever instance — avoids re-embedding the same example phrases
        # on every single chat question.
        self._overview_example_embeddings: list[list[float]] | None = None

    def retrieve(self, collection_name: str, query: str, k: int = 4) -> list[Document]:
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

    def retrieve_for_chat(
        self,
        collection_name: str,
        question: str,
        history: list[str] | None = None,
        k: int = 3,
    ) -> list[Document]:
        """
        Retrieve chunks for a chat turn, using recent turns for follow-up context.
        """

        if self.needs_broad_context(question):
            documents = self.vectorstore.get_documents(
                collection_name=collection_name,
                limit=20,
            )

            if not documents:
                raise DocumentNotFoundError(
                    "No relevant documents were found."
                )

            return documents

        retrieval_query = question

        if history:
            recent_history = "\n".join(history[-6:])
            retrieval_query = f"{recent_history}\nCurrent question: {question}"

        return self.retrieve(
            collection_name=collection_name,
            query=retrieval_query,
            k=k,
        )

    def is_overview_question(self, question: str) -> bool:
        """
        Return true if the question semantically resembles a broad
        "what is this document about" style request, using embedding
        similarity rather than literal phrase matching.
        """

        if self._overview_example_embeddings is None:
            self._overview_example_embeddings = get_embedding_model().embed_documents(
                list(OVERVIEW_EXAMPLES)
            )

        question_embedding = get_embedding_model().embed_query(question)

        similarities = [
            _cosine_similarity(question_embedding, example_embedding)
            for example_embedding in self._overview_example_embeddings
        ]

        return max(similarities) > OVERVIEW_SIMILARITY_THRESHOLD

    def needs_broad_context(self, question: str) -> bool:
        """
        Return true for questions that usually need multiple parts of a document,
        using semantic similarity against a set of known overview-style questions
        rather than brittle literal string matching.
        """

        return self.is_overview_question(question)