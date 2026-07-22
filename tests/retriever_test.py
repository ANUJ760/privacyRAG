from backend.rag.retriever import Retriever


def main():
    retriever = Retriever()

    documents = retriever.retrieve(
        collection_name="employee_handbook",
        query="What is the leave policy?",
        k=3,
    )

    for i, document in enumerate(documents, start=1):
        print(f"\nResult {i}")
        print(document.page_content)


if __name__ == "__main__":
    main()