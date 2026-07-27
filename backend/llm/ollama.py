from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage

from backend.config.settings import settings

from backend.exceptions import LLMServiceError

class LLMService:
    """
    Provides access to the configured Ollama chat model.
    """

    def __init__(self):
        self._clients: dict[str, ChatOllama] = {}

    def get_client(self, model_name: str | None = None) -> ChatOllama:
        model = model_name or settings.MODEL_NAME or settings.DEFAULT_LLM

        if model in self._clients:
            return self._clients[model]

        try:
            client = ChatOllama(
                model=model,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0,
            )
            self._clients[model] = client
            return client

        except Exception as error:
            raise LLMServiceError(
                f"Failed to initialize Ollama: {error}"
            ) from error

    def invoke(
        self,
        messages: list[BaseMessage],
        model_name: str | None = None,
    ):
        """
        Invoke the selected Ollama model.
        """

        return self.get_client(model_name).invoke(messages)

    @property
    def llm(self) -> ChatOllama:
        """
        Return the configured Ollama chat model.
        """
        return self.get_client()
