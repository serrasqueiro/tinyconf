# abase.py  (c)2020  Henrique Moreira

"""
Simplest usage of base64 and other similar bases
"""

# pylint: disable=unused-argument

import string
import base64


_ALPHABET64_RFC4648 = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"


def decoder_base64(b64_str) -> str:
    """ Decodes Base64 text ('b64_str') """
    if isinstance(b64_str, (list, tuple)):
        return decoder_base64("\n".join(b64_str))
    assert isinstance(b64_str, str)
    enter = b64_str + "==="
    bin_str = base64.b64decode(enter)
    result = bin_str.decode()
    return result


def encoder_base64(a_str) -> str:
    bin_str = base64.b64encode(bytes(a_str, "ascii"), altchars=None)
    result = bin_str.decode()
    return result


def is_base64(a_str) -> bool:
    if isinstance(a_str, (list, tuple)):
        return is_base64("\n".join(a_str))
    assert isinstance(a_str, str)
    if not a_str:
        return False
    for a_chr in a_str.rstrip("="):
        if a_chr not in _ALPHABET64_RFC4648:
            return False
    return True


# Main...
if __name__ == "__main__":
    print("Import, or see tests at abase.test.py")
