from backend.llm.ollama import LLMService
from backend.models.chat import ChatMessage
from backend.prompts.system_prompt import (
    SYSTEM_PROMPT,
    build_user_message,
)
from backend.rag.retriever import Retriever
from backend.exceptions import (
    DocumentNotFoundError,
    LLMServiceError,
    VectorStoreError,
)

class ChatService:
    """
    Handles Retrieval-Augmented Generation (RAG).
    """

    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService().llm

    def chat(
        self,
        collection_name: str,
        question: str,
        history: list[ChatMessage] | None = None,
    ) -> str:
        """
        Answer a question using the specified document collection.
        """
        history_lines = self.__format_history(history or [])

        documents = self.retriever.retrieve_for_chat(
            collection_name=collection_name,
            question=question,
            history=history_lines,
        )
        context = "\n\n".join(document.page_content for document in documents)
        print("=" * 50)
        print("Retrieved documents:")
        for i, doc in enumerate(documents):
            print(f"\nDocument {i+1}")
            print(doc.page_content[:500])
        print("=" * 50)
        response = self.llm.invoke([
            SYSTEM_PROMPT,
            build_user_message(
                context=context,
                question=question,
                history="\n".join(history_lines),
                is_overview_question=self.retriever.is_overview_question(question),
            ),
        ])

        if response is None:
            raise LLMServiceError(
                "LLM returned no response."
            )

        print("Context sent to LLM:")
        print(context)

        return response.content

    def __format_history(self, history: list[ChatMessage]) -> list[str]:
        formatted_history = []

        for message in history[-6:]:
            role = "User" if message.role == "user" else "Assistant"
            content = " ".join(message.content.split())

            if content:
                formatted_history.append(f"{role}: {content}")

        return formatted_history
