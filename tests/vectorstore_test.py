from pathlib import Path

from backend.rag.loader import DocumentLoader
from backend.rag.splitter import DocumentSplitter
from backend.rag.vectorstore import VectorStore


def main():
    loader = DocumentLoader()
    splitter = DocumentSplitter()
    vectorstore = VectorStore()

    documents = loader.load(
        Path("backend/storage/uploads/example.pdf")
    )

    chunks = splitter.split(documents)

    vectorstore.add_documents(
        collection_name="example",
        documents=chunks,
    )

    results = vectorstore.similarity_search(
        collection_name="example",
        query="What is this document about?",
        k=3,
    )

    for doc in results:
        print("-" * 50)
        print(doc.page_content)


if __name__ == "__main__":
    main()