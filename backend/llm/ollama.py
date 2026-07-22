from langchain_ollama import ChatOllama

from backend.config.settings import settings

from backend.exceptions import LLMServiceError

class LLMService:
    """
    Provides access to the configured Ollama chat model.
    """

    def __init__(self):

        try:
            self._llm = ChatOllama(
                model=settings.DEFAULT_LLM,
                temperature=0,
            )

        except Exception as error:
            raise LLMServiceError(
                f"Failed to initialize Ollama: {error}"
            ) from error

    @property
    def llm(self) -> ChatOllama:
        """
        Return the configured Ollama chat model.
        """
        return self._llm