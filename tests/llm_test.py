from backend.llm.ollama import LLMService


def main():
    llm = LLMService().llm

    response = llm.invoke("Say hello in one sentence.")

    print(response.content)


if __name__ == "__main__":
    main()