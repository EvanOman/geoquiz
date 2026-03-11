from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="south-america-countries",
    title="Countries of South America",
    description="Name all 12 countries of South America",
    map_template="maps/south_america.svg",
    time_limit=12 * 12,
    category="Continents",
    entries=[
        QuizEntry("ar", "Argentina", ["argentina"]),
        QuizEntry("bo", "Bolivia", ["bolivia"]),
        QuizEntry("br", "Brazil", ["brazil"]),
        QuizEntry("cl", "Chile", ["chile"]),
        QuizEntry("co", "Colombia", ["colombia"]),
        QuizEntry("ec", "Ecuador", ["ecuador"]),
        QuizEntry("gy", "Guyana", ["guyana"]),
        QuizEntry("py", "Paraguay", ["paraguay"]),
        QuizEntry("pe", "Peru", ["peru"]),
        QuizEntry("sr", "Suriname", ["suriname"]),
        QuizEntry("uy", "Uruguay", ["uruguay"]),
        QuizEntry("ve", "Venezuela", ["venezuela"]),
    ],
)
