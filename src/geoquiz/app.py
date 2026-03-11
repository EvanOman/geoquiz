import os
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from geoquiz.config import STATIC_DIR, TEMPLATES_DIR
from geoquiz.data.registry import all_quizzes, get_quiz, load_all

# ROOT_PATH is set when behind a reverse proxy (e.g., /geoquiz)
ROOT_PATH = os.environ.get("ROOT_PATH", "")
app = FastAPI(title="GeoQuiz", root_path=ROOT_PATH)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Register all quizzes on startup
load_all()


def _base_ctx(request: Request) -> dict:
    """Base template context with root_path for URL prefixing."""
    return {"request": request, "base": request.scope.get("root_path", "")}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    quizzes = all_quizzes()
    categories: dict[str, list] = {}
    for q in quizzes:
        categories.setdefault(q.category, []).append(q)
    return templates.TemplateResponse(
        "index.html",
        {**_base_ctx(request), "quizzes": quizzes, "categories": categories},
    )


@app.get("/quiz/{quiz_id}", response_class=HTMLResponse)
async def quiz_page(request: Request, quiz_id: str):
    quiz = get_quiz(quiz_id)
    if not quiz:
        return HTMLResponse("Quiz not found", status_code=404)

    map_path = TEMPLATES_DIR / quiz.map_template
    has_map = map_path.exists()

    return templates.TemplateResponse(
        "quiz.html",
        {**_base_ctx(request), "quiz": quiz, "has_map": has_map},
    )


@app.get("/api/quiz/{quiz_id}")
async def quiz_data(quiz_id: str):
    quiz = get_quiz(quiz_id)
    if not quiz:
        return {"error": "Quiz not found"}
    return {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "time_limit": quiz.time_limit,
        "entries": [asdict(e) for e in quiz.entries],
    }
