from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="south-america-countries",
    title="Countries of South America",
    description="Name all 12 countries of South America",
    map_template="maps/south_america.svg",
    time_limit=12 * 12,
    category="Continents",
    entries=[
        QuizEntry("ar", "Argentina", ["argentina"], label_x=3211.3, label_y=6620.3),
        QuizEntry("bo", "Bolivia", ["bolivia"], label_x=3251.9, label_y=4443.1),
        QuizEntry("br", "Brazil", ["brazil"], label_x=4944.4, label_y=3686.4),
        QuizEntry("cl", "Chile", ["chile"], label_x=2425.2, label_y=7671.6),
        QuizEntry("co", "Colombia", ["colombia"], label_x=2062.3, label_y=1610.2),
        QuizEntry("ec", "Ecuador", ["ecuador"], label_x=1488.1, label_y=2317.1),
        QuizEntry("gy", "Guyana", ["guyana"], label_x=4203.4, label_y=1501.4),
        QuizEntry("py", "Paraguay", ["paraguay"], label_x=4124.7, label_y=5406.1),
        QuizEntry("pe", "Peru", ["peru"], label_x=2051.8, label_y=3501.7),
        QuizEntry("sr", "Suriname", ["suriname"], label_x=4581.3, label_y=1563.7),
        QuizEntry("uy", "Uruguay", ["uruguay"], label_x=4124.7, label_y=6514.8),
        QuizEntry("ve", "Venezuela", ["venezuela"], label_x=3290.4, label_y=1104.1),
    ],
)
