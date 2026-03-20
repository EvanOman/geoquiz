from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="north-american-capitals",
    title="Capitals of North America",
    description="Name the capital of every North American country",
    map_template="maps/north_america.svg",
    time_limit=23 * 12,
    category="Capitals",
    entries=[
        QuizEntry("ag", "St. John's", ["st johns", "st. john's", "saint johns", "saint john's"]),
        QuizEntry("bs", "Nassau", ["nassau"]),
        QuizEntry("bb", "Bridgetown", ["bridgetown"]),
        QuizEntry("bz", "Belmopan", ["belmopan"]),
        QuizEntry("ca", "Ottawa", ["ottawa"]),
        QuizEntry("cr", "San Jose", ["san jose", "san josé"]),
        QuizEntry("cu", "Havana", ["havana", "habana", "la habana"]),
        QuizEntry("dm", "Roseau", ["roseau"]),
        QuizEntry("do", "Santo Domingo", ["santo domingo"]),
        QuizEntry("sv", "San Salvador", ["san salvador"]),
        QuizEntry(
            "gd", "St. George's", ["st georges", "st. george's", "saint georges", "saint george's"]
        ),
        QuizEntry("gt", "Guatemala City", ["guatemala city", "guatemala"]),
        QuizEntry("ht", "Port-au-Prince", ["port au prince", "port-au-prince"]),
        QuizEntry("hn", "Tegucigalpa", ["tegucigalpa"]),
        QuizEntry("jm", "Kingston", ["kingston"]),
        QuizEntry("mx", "Mexico City", ["mexico city", "ciudad de mexico", "ciudad de méxico"]),
        QuizEntry("ni", "Managua", ["managua"]),
        QuizEntry("pa", "Panama City", ["panama city", "panama"]),
        QuizEntry(
            "kn",
            "Basseterre",
            ["basseterre"],
        ),
        QuizEntry("lc", "Castries", ["castries"]),
        QuizEntry("vc", "Kingstown", ["kingstown"]),
        QuizEntry("tt", "Port of Spain", ["port of spain"]),
        QuizEntry(
            "us",
            "Washington, D.C.",
            ["washington", "washington dc", "washington d.c.", "washington d c"],
        ),
    ],
)
