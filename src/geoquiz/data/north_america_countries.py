from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="north-america-countries",
    title="Countries of North America",
    description="Name all 23 countries of North America",
    map_template="maps/north_america.svg",
    time_limit=23 * 12,
    category="Continents",
    entries=[
        QuizEntry(
            "ag",
            "Antigua and Barbuda",
            ["antigua and barbuda", "antigua", "antigua & barbuda"],
        ),
        QuizEntry("bs", "Bahamas", ["bahamas", "the bahamas"]),
        QuizEntry("bb", "Barbados", ["barbados"]),
        QuizEntry("bz", "Belize", ["belize"]),
        QuizEntry("ca", "Canada", ["canada"]),
        QuizEntry("cr", "Costa Rica", ["costa rica"]),
        QuizEntry("cu", "Cuba", ["cuba"]),
        QuizEntry("dm", "Dominica", ["dominica"]),
        QuizEntry("do", "Dominican Republic", ["dominican republic"]),
        QuizEntry("sv", "El Salvador", ["el salvador"]),
        QuizEntry("gd", "Grenada", ["grenada"]),
        QuizEntry("gt", "Guatemala", ["guatemala"]),
        QuizEntry("ht", "Haiti", ["haiti"]),
        QuizEntry("hn", "Honduras", ["honduras"]),
        QuizEntry("jm", "Jamaica", ["jamaica"]),
        QuizEntry("mx", "Mexico", ["mexico"]),
        QuizEntry("ni", "Nicaragua", ["nicaragua"]),
        QuizEntry("pa", "Panama", ["panama"]),
        QuizEntry(
            "kn",
            "Saint Kitts and Nevis",
            ["saint kitts and nevis", "st kitts and nevis", "st. kitts and nevis"],
        ),
        QuizEntry("lc", "Saint Lucia", ["saint lucia", "st lucia", "st. lucia"]),
        QuizEntry(
            "vc",
            "Saint Vincent and the Grenadines",
            [
                "saint vincent and the grenadines",
                "st vincent and the grenadines",
                "st vincent",
                "saint vincent",
            ],
        ),
        QuizEntry(
            "tt", "Trinidad and Tobago", ["trinidad and tobago", "trinidad", "trinidad & tobago"]
        ),
        QuizEntry(
            "us",
            "United States",
            ["united states", "usa", "united states of america", "us", "america"],
        ),
    ],
)
