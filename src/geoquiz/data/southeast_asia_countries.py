from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="southeast-asia-countries",
    title="Countries of Southeast Asia",
    description="Name all 11 countries of Southeast Asia",
    map_template="maps/asia.svg",
    time_limit=11 * 12,
    category="Regional",
    entries=[
        QuizEntry("bn", "Brunei", ["brunei", "brunei darussalam"]),
        QuizEntry("kh", "Cambodia", ["cambodia"]),
        QuizEntry("id", "Indonesia", ["indonesia"]),
        QuizEntry("la", "Laos", ["laos", "lao"]),
        QuizEntry("my", "Malaysia", ["malaysia"]),
        QuizEntry("mm", "Myanmar", ["myanmar", "burma"]),
        QuizEntry("ph", "Philippines", ["philippines", "the philippines"]),
        QuizEntry("sg", "Singapore", ["singapore"]),
        QuizEntry("th", "Thailand", ["thailand"]),
        QuizEntry("tl", "Timor-Leste", ["timor-leste", "east timor", "timor leste"]),
        QuizEntry("vn", "Vietnam", ["vietnam", "viet nam"]),
    ],
)
