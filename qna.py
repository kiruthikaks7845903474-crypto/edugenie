from fastapi import HTTPException

from gemini_client import GeminiGenerationError, generate_text


SYSTEM = """
You are EduGenie, an educational question-answering assistant.
Answer accurately and concisely. Explain the reasoning when useful.
Use accessible language suitable for a student. If the question is ambiguous,
state the ambiguity briefly instead of inventing facts.
"""


def answer_question(question: str) -> str:
    try:
        return generate_text(
            question,
            system_instruction=SYSTEM,
            temperature=0.3,
            max_output_tokens=1200,
        )
    except GeminiGenerationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
