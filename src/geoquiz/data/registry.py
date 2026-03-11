from dataclasses import dataclass, field


@dataclass
class QuizEntry:
    id: str
    display_name: str
    accepted_answers: list[str]


@dataclass
class Quiz:
    id: str
    title: str
    description: str
    map_template: str
    time_limit: int
    category: str
    entries: list[QuizEntry] = field(default_factory=list)


_QUIZZES: dict[str, Quiz] = {}


def register(quiz: Quiz) -> None:
    _QUIZZES[quiz.id] = quiz


def get_quiz(quiz_id: str) -> Quiz | None:
    return _QUIZZES.get(quiz_id)


def all_quizzes() -> list[Quiz]:
    return list(_QUIZZES.values())


def load_all() -> None:
    """Import all quiz modules to trigger registration."""
    from geoquiz.data import (
        africa_countries,
        asia_countries,
        europe_countries,
        north_america_countries,
        oceania_countries,
        south_america_countries,
        us_states,
    )

    for mod in [
        europe_countries,
        africa_countries,
        asia_countries,
        north_america_countries,
        south_america_countries,
        oceania_countries,
        us_states,
    ]:
        register(mod.QUIZ)
