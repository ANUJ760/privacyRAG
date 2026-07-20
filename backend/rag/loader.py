from pathlib import Path

from langchain.schema import Document
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    Docx2txtLoader,
) # loaders for PDF, DOCX, and TXT files respectively.


class DocumentLoader:
    """
    Loads supported document types into LangChain Documents.
    """

    def load(self, file_path: Path) -> list[Document]:
        """
        Load a document from disk.

        Parameters
        ----------
        file_path : Path
            Path to the uploaded document.

        Returns
        -------
        list[Document]
            LangChain Document objects.
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