from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from models import (
    ErrorResponse,
    GenerateRequest,
    QuizResponse,
    TextResponse,
)
from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": settings.gemini_configured,
        "local_explanation_enabled": settings.local_explanation_enabled,
    }


@app.post("/qa", response_model=TextResponse, responses={400: {"model": ErrorResponse}})
async def qa(payload: GenerateRequest):
    return TextResponse(result=answer_question(payload.text))


@app.post("/explain", response_model=TextResponse, responses={400: {"model": ErrorResponse}})
async def explain(payload: GenerateRequest):
    return TextResponse(result=explain_concept(payload.text))


@app.post("/quiz", response_model=QuizResponse, responses={400: {"model": ErrorResponse}})
async def quiz(payload: GenerateRequest):
    return QuizResponse(quiz=generate_quiz(payload.text))


@app.post("/summarize", response_model=TextResponse, responses={400: {"model": ErrorResponse}})
async def summarize(payload: GenerateRequest):
    return TextResponse(result=summarize_text(payload.text))


@app.post(
    "/learn/recommendations",
    response_model=TextResponse,
    responses={400: {"model": ErrorResponse}},
)
async def learning_recommendations(payload: GenerateRequest):
    return TextResponse(result=get_learning_recommendations(payload.text))
