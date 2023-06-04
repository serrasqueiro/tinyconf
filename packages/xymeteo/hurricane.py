# hurricane.py  (c)2020, 2023  Henrique Moreira

"""
List of Hurricanes and misc. data from NHC
"""

# pylint: disable=unused-argument, unnecessary-comprehension

#
# Misc hints!
#
# NHC:		National Hurricane Center
#
# see also: https://www.nhc.noaa.gov/aboutnames.shtml


import sys

_SAMPLES = (
    2020, 2021, 2022, 2023, 2024, 2025,
)

### Atlantic hurricane names!
_NAMES_2020 = (
    "Arthur",
    "Bertha",
    "Cristobal",
    "Dolly",
    "Edouard",
    "Fay",
    "Gonzalo",
    "Hanna",
    "Isaias",
    "Josephine",
    "Kyle",
    "Laura",
    "Marco",
    "Nana",
    "Omar",
    "Paulette",
    "Rene",
    "Sally",
    "Teddy",
    "Vicky",
    "Wilfred",
)

_NAMES_2021 = (
    "Ana",
    "Bill",
    "Claudette",
    "Danny",
    "Elsa",
    "Fred",
    "Grace",
    "Henri",
    "Ida",
    "Julian",
    "Kate",
    "Larry",
    "Mindy",
    "Nicholas",
    "Odette",
    "Peter",
    "Rose",
    "Sam",
    "Teresa",
    "Victor",
    "Wanda",
)

_NAMES_2022 = (
    "Alex",
    "Bonnie",
    "Colin",
    "Danielle",
    "Earl",
    "Fiona",
    "Gaston",
    "Hermine",
    "Ian",
    "Julia",
    "Karl",
    "Lisa",
    "Martin",
    "Nicole",
    "Owen",
    "Paula",
    "Richard",
    "Shary",
    "Tobias",
    "Virginie",
    "Walter",
)

_NAMES_2023 = (
    "Arlene",
    "Bret",
    "Cindy",
    "Don",
    "Emily",
    "Franklin",
    "Gert",
    "Harold",
    "Idalia",
    "Jose",
    "Katia",
    "Lee",
    "Margot",
    "Nigel",
    "Ophelia",
    "Philippe",
    "Rina",
    "Sean",
    "Tammy",
    "Vince",
    "Whitney",
)

_NAMES_2024 = (
    "Alberto",
    "Beryl",
    "Chris",
    "Debby",
    "Ernesto",
    "Francine",
    "Gordon",
    "Helene",
    "Isaac",
    "Joyce",
    "Kirk",
    "Leslie",
    "Milton",
    "Nadine",
    "Oscar",
    "Patty",
    "Rafael",
    "Sara",
    "Tony",
    "Valerie",
    "William",
)

_NAMES_2025 = (
    "Andrea",
    "Barry",
    "Chantal",
    "Dorian",
    "Erin",
    "Fernand",
    "Gabrielle",
    "Humberto",
    "Imelda",
    "Jerry",
    "Karen",
    "Lorenzo",
    "Melissa",
    "Nestor",
    "Olga",
    "Pablo",
    "Rebekah",
    "Sebastien",
    "Tanya",
    "Van",
    "Wendy",
)

_SEQ_NAMES = (
    (2020,
     ("@",
      _NAMES_2020,
      ),
    ),
    (2021,
     ("@",
      _NAMES_2021,
      ),
    ),
    (2022,
     ("@",
      _NAMES_2022,
      ),
    ),
    (2023,
     ("@",
      _NAMES_2023,
      ),
    ),
    (2024,
     ("@",
      _NAMES_2024,
      ),
    ),
    (2025,
     ("@",
      _NAMES_2025,
      ),
    ),
)

_GREEK_STORMS = (
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi",
    "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega",
)

# retired names: https://www.nhc.noaa.gov/aboutnames_history.shtml
_RETIRED_HURRICANES = (
    (1972, "Agnes"),
    (1983, "Alicia"),
    (1980, "Allen"),
    (2001, "Allison"),
    (1992, "Andrew"),
    (1977, "Anita"),
    (1957, "Audrey"),
    (1965, "Betsy"),
    (1967, "Beulah"),
    (1991, "Bob"),
    (1969, "Camille"),
    (1961, "Carla"),
    (1974, "Carmen"),
    (1954, "Carol"),
    (1970, "Celia"),
    (1996, "Cesar"),
    (2004, "Charley"),
    (1964, "Cleo"),
    (1955, "Connie"),
    (1979, "David"),
    (2007, "Dean"),
    (2005, "Dennis"),
    (1990, "Diana"),
    (1955, "Diane"),
    (1960, "Donna"),
    (1964, "Dora"),
    (1954, "Edna"),
    (1985, "Elena"),
    (1975, "Eloise"),
    (2015, "Erika"),
    (2003, "Fabian"),
    (2007, "Felix"),
    (1974, "Fifi"),
    (1963, "Flora"),
    (2018, "Florence"),
    (1999, "Floyd"),
    (1996, "Fran"),
    (2004, "Frances"),
    (1979, "Frederic"),
    (1998, "Georges"),
    (1988, "Gilbert"),
    (1985, "Gloria"),
    (1978, "Greta"),
    (2008, "Gustav"),
    (2017, "Harvey"),
    (1961, "Hattie"),
    (1954, "Hazel"),
    (1964, "Hilda"),
    (1996, "Hortense"),
    (1989, "Hugo"),
    (2010, "Igor"),
    (2008, "Ike"),
    (1966, "Inez"),
    (2013, "Ingrid"),
    (1955, "Ione"),
    (2011, "Irene"),
    (2001, "Iris"),
    (2017, "Irma"),
    (2003, "Isabel"),
    (2002, "Isidore"),
    (2004, "Ivan"),
    (1955, "Janet"),
    (2004, "Jeanne"),
    (1988, "Joan"),
    (2015, "Joaquin"),
    (2003, "Juan"),
    (2005, "Katrina"),
    (2000, "Keith"),
    (1990, "Klaus"),
    (1999, "Lenny"),
    (2002, "Lili"),
    (1995, "Luis"),
    (2017, "Maria"),
    (1995, "Marilyn"),
    (2016, "Matthew"),
    (2018, "Michael"),
    (2001, "Michelle"),
    (1998, "Mitch"),
    (2017, "Nate"),
    (2007, "Noel"),
    (1995, "Opal"),
    (2016, "Otto"),
    (2008, "Paloma"),
    (2005, "Rita"),
    (1995, "Roxanne"),
    (2012, "Sandy"),
    (2005, "Stan"),
    (2010, "Tomas"),
    (2005, "Wilma"),
)


def main():
    """ Basic simple dump of db.
    """
    code = run_main(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""{__file__} [letter]

Default letter: 'a'

a         List basic db.
""")
    sys.exit(code)


def run_main(out, err, args) -> int:
    """ Main runner """
    param = []
    if not args:
        letter = 'a'
    else:
        letter = args[0]
        param = args[1:]
    if len(letter) != 1:
        return None
    if letter == 'b':
        assert not param
        return run_b()
    if letter == 'c':
        return run_c(param)
    assert not param, "What?"
    code = run_a()
    return code


def run_a() -> int:
    """ Basic list and check! """
    for idx, pair in enumerate(_SEQ_NAMES):
        year, tup = pair
        print(":::", year, ":::", [tup])
        _, names = tup
        shown = ", ".join(names)
        listed = [name for name in names]
        check = list(_SEQ_NAMES[idx][1][1])
        print(f"{year}: {shown}")
        print("Check:", check)
        print("")
        assert _SAMPLES[idx] == year
        assert listed == check
    assert idx == 5, f"idx is: {idx}"
    return 0


def run_b() -> int:
    """ Get storms from alphabetical greek letter """
    letters = get_greek_storms()
    idx = 0
    for letter in letters:
        latin = chr(ord('A')+idx)
        print(latin, letter)
        idx += 1
    return 0


def run_c(param) -> int:
    """ Get list from year """
    value = param[0]
    rest = param[1:]
    assert not rest
    year = int(value)
    print(f"get_hurricane_names({year}):")
    names = get_hurricane_names(year)
    print(f"names (#{len(names)}: {names}")
    is_ok = 21 <= len(names) <= 26
    assert is_ok
    return 0


def get_hurricane_names(year) -> tuple:
    """ Returns the tuple of hurricanes for known year (>=2020)
    """
    invalid = ("?",)
    if year < _SAMPLES[0]:
        return invalid
    ymod = (year-2020) % 6
    names = list(_SEQ_NAMES[ymod][1][1])
    return names


def get_greek_storms() -> tuple:
    """ Returns the list (as tuple) of the storms (greek letters).
    """
    tup = _GREEK_STORMS
    assert len(tup) >= 20
    return tup


# Main...
if __name__ == "__main__":
    main()
