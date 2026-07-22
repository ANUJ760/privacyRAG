from langchain_core.messages import HumanMessage

from backend.llm.ollama import LLMService
from backend.prompts.system_prompt import SYSTEM_PROMPT
from backend.rag.retriever import Retriever


class ChatService:
    """
    Handles Retrieval-Augmented Generation (RAG).
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

        user_message = HumanMessage(
            content=f"""
            Context:{context}
            Question:{question}
        """
        )
        response = self.llm.invoke([SYSTEM_PROMPT, user_message])

        return response.content