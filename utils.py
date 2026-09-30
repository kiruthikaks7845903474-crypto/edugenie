import json
import re
from typing import Any


def clean_json_block(text: str) -> str:
    """Remove Markdown fences and surrounding prose from a JSON response."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    start = min(
        [idx for idx in (cleaned.find("["), cleaned.find("{")) if idx >= 0],
        default=-1,
    )
    if start > 0:
        cleaned = cleaned[start:]

    end_candidates = [idx for idx in (cleaned.rfind("]"), cleaned.rfind("}")) if idx >= 0]
    if end_candidates:
        cleaned = cleaned[: max(end_candidates) + 1]

    return cleaned.strip()


def parse_json_response(text: str) -> Any:
    cleaned = clean_json_block(text)
    return json.loads(cleaned)
