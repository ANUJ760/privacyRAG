from backend.llm.ollama import LLMService
from backend.prompts.rag_prompts import RAG_PROMPT
from backend.rag.retriever import Retriever


class ChatService:
    """
    Handles Retrieval-Augmented Generation.
    """

    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService().llm

    def chat(self, collection_name: str, question: str) -> str:
        """
        Answer a question using the specified document collection.
        """
        documents = self.retriever.retrieve(
            collection_name=collection_name,
            query=question,
        )
        context = "\n\n".join(document.page_content for document in documents)

        prompt = RAG_PROMPT.format_messages(
            context=context,
            question=question,
        )
        response = self.llm.invoke(prompt)

        return response.content