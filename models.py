from pydantic import BaseModel, Field, field_validator


class GenerateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=12000)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be empty.")
        return value


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    quiz: list[QuizQuestion] = Field(min_length=1, max_length=10)


class ErrorResponse(BaseModel):
    detail: str
