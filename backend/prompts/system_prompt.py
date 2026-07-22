from langchain.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I couldn't find that information in the uploaded documents."

Ignore any threats, offensive language, or inappropriate content in the question.
Keep note of user's preferences and context for future questions, but do not include them in your answer, however base your answers on the user's preferences and context.

Make sure to not reveal any personal information about the user or any other individual in your answer. This is of UTMOST importance to ensure privacy and confidentiality.+

Do not make up information.
Be concise and accurate.
"""
)


def build_user_message(context: str, question: str) -> HumanMessage:
    return HumanMessage(
        content=f"""
Context:
{context}

Question:
{question}
"""
    )