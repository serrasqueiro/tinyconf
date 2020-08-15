# abase.test.py  (c)2020  Henrique Moreira

"""
Simple tests for abase.py module
"""

# pylint: disable=unused-argument

import sys
from sys import stdin
import abase
from abase import decoder_base64, encoder_base64, \
     is_base64


def main():
    """ Main function """
    pseudo_main(sys.argv[1:])


def pseudo_main(args) -> int:
    """ Provide a simple test here. """
    alp64 = abase._ALPHABET64_RFC4648
    assert len(alp64) == 64
    if args:
        return encoding_test(args)
    print(alp64)
    print("<<<")
    code = simple_test(stdin)
    if code:
        print("Unexpected exit")
    return 0


def encoding_test(args):
    for param in args:
        text = param
        print("'{}'".format(text))
        enc_str = encoder_base64(text)
        print(enc_str)
        print("")
    return 0


def simple_test(f_in) -> int:
    """ Simple, interactive, module test. """
    lines = []
    print("Enter lines to decode Base64 strings; or a single dot ('.') to finish.\n")
    while True:
        data = f_in.readline()
        text = data.split("\n")[0]
        if text == ".":
            return 0
        if text == "":
            if lines:
                show_decoded(lines)
                print("--")
            lines = []
        else:
            is_ok = is_base64(text)
            if is_ok:
                lines.append(text)
            else:
                print("Invalid Base64 string:", text)
                return 1


def show_decoded(lines) -> bool:
    """ Show decoded string """

    def florished(a_str):
        result = a_str.replace("\t", "\\t"). \
                 replace("\n", "\\n")
        return result

    err = 0
    _joiner = ""  # "\n"
    full_str = _joiner.join(lines)
    show = "?not printable!"
    try:
        show = decoder_base64(full_str)
    except UnicodeDecodeError:
        err = 1
    if err:
        print(show)
        return False
    if show.strip() == show:
        print("decoder_base64():", show)
        print(".")
    else:
        print("decoder_base64(): '{}' !".format(florished(show)))
    assert show == decoder_base64(lines)
    enc_str = encoder_base64(show)
    if full_str != enc_str:
        print("Expected Base64 to be:", enc_str)
    return True


# Main...
if __name__ == "__main__":
    main()
