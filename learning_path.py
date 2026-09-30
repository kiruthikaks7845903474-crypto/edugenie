from fastapi import HTTPException

from gemini_client import GeminiGenerationError, generate_text


SYSTEM = """
You are EduGenie's learning-path designer.
Create practical, personalized educational roadmaps. Organize topics from
beginner to advanced. Include estimated time, goals, prerequisites, practice
ideas, and useful resource types. Do not fabricate exact URLs. If resources
are suggested, name reputable platforms or resource categories rather than
inventing links.
"""


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a structured learning path for this topic:

{topic}

Include:
1. Assumed starting level.
2. Beginner foundations.
3. Intermediate topics.
4. Advanced topics.
5. A suggested timeline.
6. Practice/project ideas.
7. Recommended resource types or reputable platforms.
8. A simple next step the learner can do today.
"""
    try:
        return generate_text(
            prompt,
            system_instruction=SYSTEM,
            temperature=0.55,
            max_output_tokens=2400,
        )
    except GeminiGenerationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
