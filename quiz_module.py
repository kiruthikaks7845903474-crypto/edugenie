from fastapi import HTTPException

from gemini_client import GeminiGenerationError, generate_text
from models import QuizQuestion
from utils import parse_json_response


SYSTEM = """
You are EduGenie's quiz generator.
Create educational multiple-choice questions from the supplied topic or
passage. Return ONLY valid JSON: an array of exactly three objects.
Each object must have:
- question: string
- options: array of exactly four distinct strings
- correct_answer: string that exactly matches one option
- explanation: short explanation of why the answer is correct

Questions must be answerable from the supplied material or ordinary
well-established facts about the requested topic. Avoid trick questions.
"""


def _validate_quiz(data) -> list[QuizQuestion]:
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Gemini did not return exactly three quiz questions.")

    result = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is not a JSON object.")

        question = str(item.get("question", "")).strip()
        options = item.get("options")
        correct = str(item.get("correct_answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must contain four options.")

        options = [str(option).strip() for option in options]
        if len(set(options)) != 4:
            raise ValueError(f"Question {index} contains duplicate options.")

        if correct not in options:
            raise ValueError(
                f"Question {index}'s correct_answer must exactly match an option."
            )

        result.append(
            QuizQuestion(
                question=question,
                options=options,
                correct_answer=correct,
                explanation=explanation,
            )
        )

    return result


def generate_quiz(text: str) -> list[QuizQuestion]:
    prompt = f"""
Generate a three-question MCQ quiz from the following topic or passage.

SOURCE:
{text}
"""
    try:
        raw = generate_text(
            prompt,
            system_instruction=SYSTEM,
            temperature=0.45,
            max_output_tokens=2200,
        )
        return _validate_quiz(parse_json_response(raw))
    except (GeminiGenerationError, ValueError, TypeError, KeyError) as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Quiz generation failed: {exc}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not parse quiz response: {exc}",
        ) from exc
