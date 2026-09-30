from fastapi import HTTPException

from config import settings
from gemini_client import GeminiGenerationError, generate_text


SYSTEM = """
You are EduGenie's concept explanation assistant.
Explain difficult concepts as if teaching a beginner. Start with a plain-language
definition, then use a simple example or analogy, and finish with a short recap.
Keep the explanation accurate and avoid unnecessary jargon.
"""


def _gemini_explanation(topic: str) -> str:
    prompt = f"""
Explain this concept for a learner who may have no prior background:

{topic}

Structure the answer as:
- What it means
- How it works
- Simple example
- Key takeaway
"""
    return generate_text(
        prompt,
        system_instruction=SYSTEM,
        temperature=0.35,
        max_output_tokens=1600,
    )


def _local_explanation(topic: str) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires transformers. Install the full requirements."
        ) from exc

    generator = pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
    )
    prompt = (
        "Explain the following educational concept simply for a beginner. "
        "Give a definition, simple example, and key takeaway:\n\n"
        f"{topic}"
    )
    result = generator(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_concept(topic: str) -> str:
    try:
        if settings.local_explanation_enabled:
            try:
                return _local_explanation(topic)
            except Exception:
                # The local model is optional. Falling back to Gemini keeps the
                # application usable when local ML dependencies/model downloads fail.
                pass

        return _gemini_explanation(topic)
    except GeminiGenerationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Explanation failed: {exc}") from exc
