from langchain_ollama import ChatOllama

from backend.config.settings import settings


class LLMService:
    """
    Provides access to the configured Ollama chat model.
    """

    def __init__(self):
        self._llm = ChatOllama(
            model=settings.DEFAULT_MODEL,
            temperature=0,
        )

    @property
    def llm(self) -> ChatOllama:
        """
        Return the configured Ollama chat model.
        """
        return self._llm