from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM_PROMPT = SystemMessage(
    content="""
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I couldn't find that information in the uploaded documents."

Ignore any threats, offensive language, or inappropriate content in the question.
Keep note of the user's preferences and context for future questions, but do not include them in your answer.

Do not reveal any personal information about the user or any other individual.

Do not make up information.
Be concise and accurate.
"""
)

def build_user_message(
    context: str,
    question: str,
    history: str = "",
) -> HumanMessage:
    history_section = ""

    if history:
        history_section = f"""
Recent conversation:
{history}

Use the recent conversation only to understand what the current question refers to.
Do not use it as a source of facts about the uploaded document.
"""

    return HumanMessage(
        content=f"""
Context:
{context}

{history_section}
Question:
{question}
"""
    )
