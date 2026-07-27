from langchain_core.documents import Document

from backend.config.settings import settings
from backend.llm.ollama import LLMService
from backend.models.chat import ChatMessage
from backend.prompts.system_prompt import (
    SYSTEM_PROMPT,
    build_user_message,
)
from backend.rag.retriever import Retriever
from backend.exceptions import InvalidModelError, LLMServiceError


class ChatService:
    """
    Handles Retrieval-Augmented Generation (RAG).
    """

    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService()

    def chat(
        self,
        collection_name: str,
        question: str,
        history: list[ChatMessage] | None = None,
        model_name: str | None = None,
    ) -> str:
        """
        Answer a question using the specified document collection.
        """
        selected_model = self.__resolve_model(model_name)
        history_lines = self.__format_history(history or [])

        documents = self.retriever.retrieve_for_chat(
            collection_name=collection_name,
            question=question,
            history=history_lines,
        )
        context = self.__format_context(documents)
        print("=" * 50)
        print("Retrieved documents:")
        for i, doc in enumerate(documents):
            print(f"\nDocument {i+1}")
            print(doc.page_content[:500])
        print("=" * 50)
        response = self.llm.invoke(
            [
                SYSTEM_PROMPT,
                build_user_message(
                    context=context,
                    question=question,
                    history="\n".join(history_lines),
                    is_overview_question=self.retriever.is_overview_question(question),
                ),
            ],
            model_name=selected_model,
        )

        if response is None:
            raise LLMServiceError(
                "LLM returned no response."
            )

        print("Context sent to LLM:")
        print(context)

        return response.content.strip()

    def get_model_options(self) -> dict:
        return {
            "default_model": settings.MODEL_NAME,
            "models": settings.MODEL_OPTIONS,
        }

    def __resolve_model(self, model_name: str | None) -> str:
        selected_model = (model_name or settings.MODEL_NAME).strip()

        if selected_model not in settings.MODEL_OPTIONS:
            raise InvalidModelError(
                f"Model '{selected_model}' is not enabled for this deployment."
            )

        return selected_model

    def __format_context(self, documents: list[Document]) -> str:
        context_blocks = []

        for index, document in enumerate(documents, start=1):
            metadata = document.metadata or {}
            source = metadata.get("source") or metadata.get("file_path")
            page = metadata.get("page")
            source_parts = [f"Chunk {index}"]

            if source:
                source_parts.append(f"source: {source}")

            if page is not None:
                source_parts.append(f"page: {page}")

            context_blocks.append(
                f"[{'; '.join(source_parts)}]\n{document.page_content}"
            )

        return "\n\n".join(context_blocks)

    def __format_history(self, history: list[ChatMessage]) -> list[str]:
        formatted_history = []

        for message in history[-6:]:
            role = "User" if message.role == "user" else "Assistant"
            content = " ".join(message.content.split())

            if content:
                formatted_history.append(f"{role}: {content}")

        return formatted_history
