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
        QuizEntry("bs", "Bahamas", ["bahamas", "the bahamas"], label_x=901.9, label_y=878.0),
        QuizEntry("bb", "Barbados", ["barbados"], label_x=1157.2, label_y=943.5),
        QuizEntry("bz", "Belize", ["belize"], label_x=753.0, label_y=1007.0),
        QuizEntry("ca", "Canada", ["canada"], label_x=670.0, label_y=332.3),
        QuizEntry("cr", "Costa Rica", ["costa rica"]),
        QuizEntry("cu", "Cuba", ["cuba"], label_x=867.0, label_y=922.8),
        QuizEntry("dm", "Dominica", ["dominica"], label_x=1124.8, label_y=924.8),
        QuizEntry("do", "Dominican Republic", ["dominican republic"]),
        QuizEntry("sv", "El Salvador", ["el salvador"]),
        QuizEntry("gd", "Grenada", ["grenada"], label_x=1134.2, label_y=969.6),
        QuizEntry("gt", "Guatemala", ["guatemala"], label_x=729.5, label_y=1030.6),
        QuizEntry("ht", "Haiti", ["haiti"], label_x=962.3, label_y=938.3),
        QuizEntry("hn", "Honduras", ["honduras"], label_x=790.1, label_y=1035.8),
        QuizEntry("jm", "Jamaica", ["jamaica"], label_x=906.1, label_y=966.1),
        QuizEntry("mx", "Mexico", ["mexico"], label_x=549.9, label_y=918.3),
        QuizEntry("ni", "Nicaragua", ["nicaragua"], label_x=810.4, label_y=1058.8),
        QuizEntry("pa", "Panama", ["panama"], label_x=885.2, label_y=1107.1),
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
