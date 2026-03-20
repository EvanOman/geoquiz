from dataclasses import asdict

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from geoquiz.config import STATIC_DIR, TEMPLATES_DIR
from geoquiz.data.registry import all_quizzes, get_quiz, load_all

app = FastAPI(title="GeoQuiz")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Register all quizzes on startup
load_all()


CATEGORY_ORDER = ["Continents", "Capitals", "United States", "Regional", "History", "Trivia"]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    quizzes = all_quizzes()
    categories: dict[str, list] = {}
    for q in quizzes:
        categories.setdefault(q.category, []).append(q)
    ordered = [(cat, categories[cat]) for cat in CATEGORY_ORDER if cat in categories]
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "quizzes": quizzes, "categories": ordered},
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
        {"request": request, "quiz": quiz, "has_map": has_map},
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
