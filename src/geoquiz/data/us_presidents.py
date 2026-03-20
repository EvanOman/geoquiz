from geoquiz.data.registry import Quiz, QuizEntry

QUIZ = Quiz(
    id="us-presidents",
    title="US Presidents",
    description="Name all 45 unique Presidents of the United States",
    time_limit=45 * 12,
    category="History",
    entries=[
        QuizEntry("p01", "George Washington", ["washington", "george washington"]),
        QuizEntry("p02", "John Adams", ["adams", "john adams"]),
        QuizEntry("p03", "Thomas Jefferson", ["jefferson", "thomas jefferson"]),
        QuizEntry("p04", "James Madison", ["madison", "james madison"]),
        QuizEntry("p05", "James Monroe", ["monroe", "james monroe"]),
        QuizEntry("p06", "John Quincy Adams", ["john quincy adams", "quincy adams", "jq adams"]),
        QuizEntry("p07", "Andrew Jackson", ["jackson", "andrew jackson"]),
        QuizEntry("p08", "Martin Van Buren", ["van buren", "martin van buren"]),
        QuizEntry("p09", "William Henry Harrison", ["harrison", "william henry harrison"]),
        QuizEntry("p10", "John Tyler", ["tyler", "john tyler"]),
        QuizEntry("p11", "James K. Polk", ["polk", "james polk", "james k polk"]),
        QuizEntry("p12", "Zachary Taylor", ["taylor", "zachary taylor"]),
        QuizEntry("p13", "Millard Fillmore", ["fillmore", "millard fillmore"]),
        QuizEntry("p14", "Franklin Pierce", ["pierce", "franklin pierce"]),
        QuizEntry("p15", "James Buchanan", ["buchanan", "james buchanan"]),
        QuizEntry("p16", "Abraham Lincoln", ["lincoln", "abraham lincoln", "abe lincoln"]),
        QuizEntry("p17", "Andrew Johnson", ["johnson", "andrew johnson"]),
        QuizEntry("p18", "Ulysses S. Grant", ["grant", "ulysses grant", "ulysses s grant"]),
        QuizEntry(
            "p19", "Rutherford B. Hayes", ["hayes", "rutherford hayes", "rutherford b hayes"]
        ),
        QuizEntry("p20", "James A. Garfield", ["garfield", "james garfield", "james a garfield"]),
        QuizEntry("p21", "Chester A. Arthur", ["arthur", "chester arthur", "chester a arthur"]),
        QuizEntry("p22", "Grover Cleveland", ["cleveland", "grover cleveland"]),
        QuizEntry("p23", "Benjamin Harrison", ["benjamin harrison", "ben harrison"]),
        QuizEntry("p24", "William McKinley", ["mckinley", "william mckinley"]),
        QuizEntry(
            "p25", "Theodore Roosevelt", ["roosevelt", "theodore roosevelt", "teddy roosevelt"]
        ),
        QuizEntry("p26", "William Howard Taft", ["taft", "william taft", "william howard taft"]),
        QuizEntry("p27", "Woodrow Wilson", ["wilson", "woodrow wilson"]),
        QuizEntry("p28", "Warren G. Harding", ["harding", "warren harding", "warren g harding"]),
        QuizEntry("p29", "Calvin Coolidge", ["coolidge", "calvin coolidge"]),
        QuizEntry("p30", "Herbert Hoover", ["hoover", "herbert hoover"]),
        QuizEntry(
            "p31", "Franklin D. Roosevelt", ["franklin roosevelt", "franklin d roosevelt", "fdr"]
        ),
        QuizEntry("p32", "Harry S. Truman", ["truman", "harry truman", "harry s truman"]),
        QuizEntry(
            "p33",
            "Dwight D. Eisenhower",
            ["eisenhower", "dwight eisenhower", "dwight d eisenhower", "ike"],
        ),
        QuizEntry("p34", "John F. Kennedy", ["kennedy", "john kennedy", "john f kennedy", "jfk"]),
        QuizEntry("p35", "Lyndon B. Johnson", ["lyndon johnson", "lyndon b johnson", "lbj"]),
        QuizEntry("p36", "Richard Nixon", ["nixon", "richard nixon"]),
        QuizEntry("p37", "Gerald Ford", ["ford", "gerald ford"]),
        QuizEntry("p38", "Jimmy Carter", ["carter", "jimmy carter", "james carter"]),
        QuizEntry("p39", "Ronald Reagan", ["reagan", "ronald reagan"]),
        QuizEntry(
            "p40", "George H.W. Bush", ["bush", "george bush", "george hw bush", "george h w bush"]
        ),
        QuizEntry("p41", "Bill Clinton", ["clinton", "bill clinton", "william clinton"]),
        QuizEntry("p42", "George W. Bush", ["george w bush", "w bush"]),
        QuizEntry("p43", "Barack Obama", ["obama", "barack obama"]),
        QuizEntry("p44", "Donald Trump", ["trump", "donald trump"]),
        QuizEntry("p45", "Joe Biden", ["biden", "joe biden", "joseph biden"]),
    ],
)
