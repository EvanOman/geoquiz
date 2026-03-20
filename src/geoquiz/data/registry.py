from dataclasses import dataclass, field


@dataclass
class QuizEntry:
    id: str
    display_name: str
    accepted_answers: list[str]
    label_x: float | None = None
    label_y: float | None = None


@dataclass
class Quiz:
    id: str
    title: str
    description: str
    time_limit: int
    category: str
    map_template: str | None = None
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
        african_capitals,
        asia_countries,
        asian_capitals,
        eu_member_states,
        europe_countries,
        european_capitals,
        largest_countries,
        middle_east_countries,
        nato_member_states,
        north_america_countries,
        north_american_capitals,
        oceania_countries,
        south_america_countries,
        south_american_capitals,
        southeast_asia_countries,
        us_presidents,
        us_state_capitals,
        us_states,
    )

    for mod in [
        europe_countries,
        european_capitals,
        africa_countries,
        african_capitals,
        asia_countries,
        asian_capitals,
        north_america_countries,
        north_american_capitals,
        south_america_countries,
        south_american_capitals,
        oceania_countries,
        us_states,
        us_state_capitals,
        eu_member_states,
        nato_member_states,
        middle_east_countries,
        southeast_asia_countries,
        us_presidents,
        largest_countries,
    ]:
        register(mod.QUIZ)
