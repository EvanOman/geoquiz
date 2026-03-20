from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="south-american-capitals",
    title="Capitals of South America",
    description="Name the capital of every South American country",
    map_template="maps/south_america.svg",
    time_limit=12 * 12,
    category="Capitals",
    entries=[
        QuizEntry("ar", "Buenos Aires", ["buenos aires"]),
        QuizEntry("bo", "Sucre", ["sucre", "la paz"]),
        QuizEntry("br", "Brasilia", ["brasilia"]),
        QuizEntry("cl", "Santiago", ["santiago"]),
        QuizEntry("co", "Bogota", ["bogota", "bogotá"]),
        QuizEntry("ec", "Quito", ["quito"]),
        QuizEntry("gy", "Georgetown", ["georgetown"]),
        QuizEntry("py", "Asuncion", ["asuncion", "asunción"]),
        QuizEntry("pe", "Lima", ["lima"]),
        QuizEntry("sr", "Paramaribo", ["paramaribo"]),
        QuizEntry("uy", "Montevideo", ["montevideo"]),
        QuizEntry("ve", "Caracas", ["caracas"]),
    ],
)
