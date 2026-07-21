from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config.settings import settings


class DocumentSplitter:
    # split the document into chunks of text with a specified chunk size and overlap.
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
    # split_documents is a in-built method of RecursiveCharacterTextSPlitter.
    def split(self, documents: list[Document]) -> list[Document]:

        return self.text_splitter.split_documents(documents) 
