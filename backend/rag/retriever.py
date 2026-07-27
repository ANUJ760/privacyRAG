import re

from langchain_core.documents import Document

from backend.rag.vectorstore import VectorStore

from backend.exceptions import DocumentNotFoundError


class Retriever:
    """
    Retrieves relevant document chunks from the vector store.
    """

    def __init__(self):
        self.vectorstore = VectorStore()

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
        k: int = 6,
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

    def needs_broad_context(self, question: str) -> bool:
        """
        Return true for questions that usually need multiple parts of a document.
        """

        normalized = " ".join(question.lower().split())

        broad_patterns = (
            r"\ball\b",
            r"\bany\b",
            "compare",
            "comparison",
            "differences",
            "differentiate",
            "extract",
            "find every",
            "list",
            "main points",
            "requirements",
            "responsibilities",
            "risks",
            "table",
            "timeline",
            "what are the",
        )

        return self.is_overview_question(question) or any(
            re.search(pattern, normalized) for pattern in broad_patterns
        )

    def is_overview_question(self, question: str) -> bool:
        normalized = " ".join(question.lower().split())

        overview_phrases = (
            "what is the file about",
            "what is this file about",
            "what is the document about",
            "what is this document about",
            "what's the file about",
            "whats the file about",
            "tell me about the file",
            "tell me about this file",
            "explain the file",
            "explain about the file",
            "explain this file",
            "explain the document",
            "explain this document",
            "what is inside",
            "what's inside",
            "whats inside",
            "what does it contain",
            "what does this contain",
            "summarize",
            "summary",
            "overview",
        )

        return any(phrase in normalized for phrase in overview_phrases)
