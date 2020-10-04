# latin1.py  (c)2020  Henrique Moreira

"""
Remove accents in latin-1
"""

# pylint: disable=unused-argument

import unicodedata

def strip_accents(a_str) -> str:
    """ Strip accents from string.
    Converts strings such as
	a' (a with acute accent)
	c, (c cedil)
    to the original ASCII chars, e.g. 'a' and 'c' in the previous examples.
    """
    if not isinstance(a_str, str):
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', a_str)
                   if unicodedata.category(c) != 'Mn')


# Main...
if __name__ == "__main__":
    print("Import!")
