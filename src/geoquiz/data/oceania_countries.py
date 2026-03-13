from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="oceania-countries",
    title="Countries of Oceania",
    description="Name all 14 countries of Oceania",
    map_template="maps/oceania.svg",
    time_limit=14 * 12,
    category="Continents",
    entries=[
        QuizEntry("au", "Australia", ["australia"], label_x=90.5, label_y=141.2),
        QuizEntry("fj", "Fiji", ["fiji"]),
        QuizEntry("ki", "Kiribati", ["kiribati"]),
        QuizEntry("mh", "Marshall Islands", ["marshall islands"]),
        QuizEntry("fm", "Micronesia", ["micronesia", "federated states of micronesia", "fsm"]),
        QuizEntry("nr", "Nauru", ["nauru"]),
        QuizEntry("nz", "New Zealand", ["new zealand", "aotearoa", "nz"], label_x=162.5, label_y=179.1),
        QuizEntry("pw", "Palau", ["palau"]),
        QuizEntry("pg", "Papua New Guinea", ["papua new guinea", "png"], label_x=67.3, label_y=78.8),
        QuizEntry("ws", "Samoa", ["samoa", "western samoa"]),
        QuizEntry("sb", "Solomon Islands", ["solomon islands"], label_x=113.0, label_y=84.9),
        QuizEntry("to", "Tonga", ["tonga"]),
        QuizEntry("tv", "Tuvalu", ["tuvalu"]),
        QuizEntry("vu", "Vanuatu", ["vanuatu"]),
    ],
)
