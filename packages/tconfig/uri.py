"""
URI - Universal Resource Identifier

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=unused-argument, superfluous-parens, invalid-name, no-self-use

### Because you force an assignment of a protected attribute:
# pylint: disable=protected-access

import sys


def tests():
    """ A few unit tests for this module.
    """
    args = sys.argv[1:]
    is_ok = run_tests(args)
    assert is_ok


def run_tests(args):
    """ Main/ basic tests
    """
    param = []
    if args:
        what = args[0]
        param = args[1:]
    else:
        what = None
    in_file = open(what, "r") if what else sys.stdin
    out_file = sys.stdout
    assert param == []
    is_ok = run_test(out_file, in_file)
    return is_ok


def run_test(out_file, in_file, debug=0):
    """ Simple test
    """
    lines = in_file.read().split("\n")
    uri = None
    for line in lines:
        uri = URI(line)
        uri.process()
        s = uri.raw()
        s_base = uri.base()
        duo = URI(s_base, auto_process=True)
        xtra = ""
        xtra = '\n"{}"'.format(duo)
        if s == "":
            continue
        if str(duo) == line:
            s_ok = "OK"
        elif s_base:
            s_ok = "SeemOk"
        else:
            s_ok = "NotOk"
        out_file.write("'{}', {}\nraw()='{}'\nstr()='{}'\nbase()={}{}\n\n"
                       "".format(line, s_ok, s, uri, s_base if s_base else "<empty>", xtra))
    if uri is None:
        return True
    if debug > 0:
        print("Basic valid chars are now...:", " ".join(uri.basic_valid))
        uri._BASIC_VALID = ('/',)
        print("Basic valid chars are still.:", " ".join(uri.basic_valid))
    return True


class URI():
    """
    Universal Resource Identifier generic class
    """
    name = ""
    _complete = ""
    _visible = None
    _base = None  # No %xx (hex) strings
    # Valid chrs in a URI, not changed into '%xx' (hex):
    _BASIC_VALID = ('/', ':', '-', '_', '?', '=',
                    ',', '#', '.', '~', '%',
                    )

    @property
    def basic_valid(self):
        """ Immutable 'static' """
        # 'basic_valid' is immutable
        return type(self)._BASIC_VALID


    def __init__(self, path="", name="", auto_process=False):
        """ Basic class init """
        self.name, self._complete = name, path
        if auto_process:
            self.process()


    def __str__(self):
        """ Redefined string """
        return self._visible


    def process(self, new_path=None):
        """ Process obj. related data """
        if new_path is None:
            p = self._complete
        else:
            p = new_path
        s = p.strip().replace("\\", "/")
        self._complete = s
        if self._set_visible(self._complete):
            self._base = self._get_from_hex_str(self._visible)
        else:
            self._base = ""
        return s


    def base(self):
        """ Return the base URI string; free of %xx hex, easier to read """
        return self._base


    def raw(self):
        """ Return the raw URI string """
        return self._complete


    def _set_visible(self, s):
        """ Only stores valid chars at '_visible' string
        """
        res = ""
        bogus = None
        if isinstance(s, str):
            if s.find(": ") < 0 and s.find("# ") < 0:
                res, bogus = self._get_visible_from_string(s, skip_quotes=True)
        else:
            assert False
        self._visible = res
        is_ok = bogus is None or bogus[1] == []
        return is_ok


    def _get_visible_from_string(self, s, skip_quotes=False):
        """ Returns only the visible chars
        """
        res = ""
        bad = list()
        valid_chrs = self.basic_valid
        in_str = s
        if len(s) >= 2:
            if skip_quotes and s[0] in ("'", '"'):
                quote = s[0]
                if s[-1] == quote:
                    in_str = s[1:-1]
        in_str = in_str.strip().replace("%%", "%")
        quotes = in_str.count('"')
        for c in in_str:
            d = ord(c)
            v = None
            if c < ' ' or d >= 127:
                bad.append(c)
            elif c in valid_chrs or c.isalnum():
                v = c
            else:
                v = "%{:02X}".format(d)
                if (quotes % 2) == 1:
                    bad.append(c)  # even number of quotes!
            if v is not None:
                res += v
        bogus = (in_str, bad)
        return (res, bogus)


    def _get_from_hex_str(self, s):
        """ Returns a base string, without '%xx' hex references """
        assert isinstance(s, str)
        res = ""
        idx = 0
        while idx < len(s):
            c, inc = s[idx], 1
            val = None
            if c == "%":
                tuc = s[idx+1:idx+3]
                try:
                    val = int(tuc, 16)
                    inc += 2
                except ValueError:
                    val = None
            if val is None:
                res += c
            else:
                res += self._acceptable_decimal(val)
            idx += inc
        return res


    def _acceptable_decimal(self, val, default="?"):
        assert isinstance(val, int)
        if 32 <= val <= 255 and not (0x7F <= val <= 192):
            return chr(val)
        return default


def split_domain(s):
    assert isinstance(s, str)
    pre = ""
    post = ""
    pos = s.find("/")
    if pos == -1:
        pre = s
    else:
        pre = s[:pos]
        post = s[pos+1:]
    return (pre, post)


if __name__ == "__main__":
    print("Import this module; follow a few tests.")
    tests()
