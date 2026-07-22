from pathlib import Path

from backend.rag.loader import DocumentLoader
from backend.rag.splitter import DocumentSplitter


def main():
    loader = DocumentLoader()
    splitter = DocumentSplitter()

    documents = loader.load(
        Path("backend/storage/uploads/example.pdf")
    )

    chunks = splitter.split(documents)

    print(f"Created {len(chunks)} chunks.")

    print(chunks[0].page_content)


if __name__ == "__main__":
    main()