from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="middle-east-countries",
    title="Countries of the Middle East",
    description="Name all 16 countries of the Middle East",
    map_template="maps/asia.svg",
    time_limit=16 * 12,
    category="Regional",
    entries=[
        QuizEntry("bh", "Bahrain", ["bahrain"]),
        QuizEntry("cy", "Cyprus", ["cyprus"]),
        QuizEntry("ir", "Iran", ["iran", "persia", "islamic republic of iran"]),
        QuizEntry("iq", "Iraq", ["iraq"]),
        QuizEntry("il", "Israel", ["israel"]),
        QuizEntry("jo", "Jordan", ["jordan"]),
        QuizEntry("kw", "Kuwait", ["kuwait"]),
        QuizEntry("lb", "Lebanon", ["lebanon"]),
        QuizEntry("om", "Oman", ["oman"]),
        QuizEntry("ps", "Palestine", ["palestine", "state of palestine"]),
        QuizEntry("qa", "Qatar", ["qatar"]),
        QuizEntry("sa", "Saudi Arabia", ["saudi arabia"]),
        QuizEntry("sy", "Syria", ["syria"]),
        QuizEntry("tr", "Turkey", ["turkey", "turkiye"]),
        QuizEntry(
            "ae",
            "United Arab Emirates",
            ["united arab emirates", "uae", "emirates"],
        ),
        QuizEntry("ye", "Yemen", ["yemen"]),
    ],
)
