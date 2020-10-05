# hurricane.py  (c)2020  Henrique Moreira

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

_SAMPLES = (2020, 2021, 2022, 2023, 2024, 2025,
            )
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

_SEQ_NAMES = ((2020,
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
    param = list()
    if not args:
        letter = 'a'
    else:
        letter = args[0]
        param = args[1:]
    if len(letter) != 1:
        return None
    assert not param
    code = run_a()
    return code


def run_a() -> int:
    """ Basic list and check! """
    idx = 0
    for year, tup in _SEQ_NAMES:
        _, names = tup
        shown = ", ".join(names)
        listed = [name for name in names]
        check = list(_SEQ_NAMES[idx][1][1])
        print(f"{year}: {shown}")
        print("Check:", check)
        print("")
        assert _SAMPLES[idx] == year
        assert listed == check
        idx += 1
    assert idx == 6
    return 0


# Main...
if __name__ == "__main__":
    main()
