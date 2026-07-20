from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config.settings import settings


class DocumentSplitter:
    """
    Splits LangChain documents into smaller overlapping chunks.
    """

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split(self, documents: list[Document]) -> list[Document]:
        """
        Split documents into smaller chunks.

        Parameters
        ----------
        documents : list[Document]

        Returns
        -------
        list[Document]
        """

        return self.text_splitter.split_documents(documents)
