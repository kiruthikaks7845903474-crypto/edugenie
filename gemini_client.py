from functools import lru_cache

from google import genai
from google.genai import types

from config import settings


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini cannot be used because configuration is missing."""


class GeminiGenerationError(RuntimeError):
    """Raised when Gemini generation fails."""


@lru_cache
def get_client() -> genai.Client:
    if not settings.gemini_configured:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. Add it to the .env file."
        )
    try:
        return genai.Client(api_key=settings.gemini_api_key)
    except Exception as exc:
        raise GeminiConfigurationError(
            f"Could not initialize Gemini client: {exc}"
        ) from exc


def generate_text(
    prompt: str,
    *,
    system_instruction: str,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
) -> str:
    try:
        client = get_client()
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise GeminiGenerationError("Gemini returned an empty response.")
        return text
    except (GeminiConfigurationError, GeminiGenerationError):
        raise
    except Exception as exc:
        raise GeminiGenerationError(f"Gemini request failed: {exc}") from exc
