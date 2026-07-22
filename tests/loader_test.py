from pathlib import Path

from backend.rag.loader import DocumentLoader


def main():
    loader = DocumentLoader()

    documents = loader.load(
        Path("backend/storage/uploads/example.pdf")
    )

    print(f"Loaded {len(documents)} pages.")

    print(documents[0].page_content[:500])


if __name__ == "__main__":
    main()