from fastapi import HTTPException

from gemini_client import GeminiGenerationError, generate_text


SYSTEM = """
You are EduGenie's summarization assistant.
Summarize educational material clearly and faithfully. Preserve important
facts, terminology, relationships, and conclusions. Remove repetition.
Return a concise summary with short paragraphs or bullet points when that
improves readability. Do not add information that is not supported by the input.
"""


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for quick revision.

PASSAGE:
{text}
"""
    try:
        return generate_text(
            prompt,
            system_instruction=SYSTEM,
            temperature=0.25,
            max_output_tokens=1600,
        )
    except GeminiGenerationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
