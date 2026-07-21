from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    Docx2txtLoader,
) # loaders for PDF, DOCX, and TXT files respectively.


class DocumentLoader:

    def load(self, file_path: Path) -> list[Document]:
        """
        Load a supported document file into LangChain Document objects.

        Args:
            file_path: Path to a PDF, DOCX, or TXT file on disk.
        """

        extension = file_path.suffix.lower() # file extension (.pdf, .docx, .txt, etc)

        if extension == ".pdf":
            loader = PyMuPDFLoader(str(file_path))

        elif extension == ".docx":
            loader = Docx2txtLoader(str(file_path))

        elif extension == ".txt":
            loader = TextLoader(
                str(file_path),
                encoding="utf-8",
            )

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return loader.load()
