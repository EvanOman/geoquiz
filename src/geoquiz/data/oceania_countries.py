from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="oceania-countries",
    title="Countries of Oceania",
    description="Name all 14 countries of Oceania",
    map_template="maps/oceania.svg",
    time_limit=14 * 12,
    category="Continents",
    entries=[
        QuizEntry("au", "Australia", ["australia"]),
        QuizEntry("fj", "Fiji", ["fiji"]),
        QuizEntry("ki", "Kiribati", ["kiribati"]),
        QuizEntry("mh", "Marshall Islands", ["marshall islands"]),
        QuizEntry("fm", "Micronesia", ["micronesia", "federated states of micronesia", "fsm"]),
        QuizEntry("nr", "Nauru", ["nauru"]),
        QuizEntry("nz", "New Zealand", ["new zealand", "aotearoa", "nz"]),
        QuizEntry("pw", "Palau", ["palau"]),
        QuizEntry("pg", "Papua New Guinea", ["papua new guinea", "png"]),
        QuizEntry("ws", "Samoa", ["samoa", "western samoa"]),
        QuizEntry("sb", "Solomon Islands", ["solomon islands"]),
        QuizEntry("to", "Tonga", ["tonga"]),
        QuizEntry("tv", "Tuvalu", ["tuvalu"]),
        QuizEntry("vu", "Vanuatu", ["vanuatu"]),
    ],
)
