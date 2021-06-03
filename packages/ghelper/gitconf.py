
# (c)2021  Henrique Moreira (h@serrasqueiro.com)

"""
(a simple) git configuration reader
"""

# pylint: disable=unused-argument

import sys
import re

def main():
    """ Main script """
    code = run_script(sys.argv[1:])
    sys.exit(code if code else 0)

def run_script(args):
    """ Run script """
    verbose = 0
    param = args
    while param and param[0].startswith("-"):
        if param[0] == "-v":
            verbose += 1
            del param[0]
            continue
        return None
    if not param:
        streams = [("", sys.stdin)]
    else:
        streams = [(fname, open(fname, "r")) for fname in param]
    for fname, stream in streams:
        gconf = GitConf(stream.read(), fname)
        url_info = gconf.get_items("url-info")
        if verbose > 0:
            aname = f"{fname}: " if fname else ""
            shown = ', '.join([f"{kind}={url}" for kind, url in url_info])
            print(f"{aname}{shown}")
        else:
            alist = gconf.get_urls()
            print(', '.join(alist))
    return 0


class TextConf():
    """ Textual Configuration (abstract) """
    _name = ""
    _data = ""
    _code = -1

    def named(self) -> str:
        """ Return filename/ designation """
        return self._name

class GitConf(TextConf):
    """ GitConf class handles text config files from .git/... """
    _keys = None

    """ Git Configuration File (simple) reader """
    def __init__(self, data:str, fname:str=""):
        """ Initializer """
        self._data = data
        self._name = fname
        self._code = self._parse(data)

    def get_items(self, keyname:str):
        """ Return the item designated by the 'keyname'.
        """
        return self._keys[keyname]

    def a_token(self, astr) -> list:
        """ Returns a list for the complete token, e.g. 'remote "origin"'
        """
        what = self._keys["@original"].get(astr)
        if not what:
            return list()
        return what

    def b_token(self, astr) -> list:
        """ Returns a list for the complete token, e.g. 'remote-origin'
        """
        what = self._keys["@original"].get(astr)
        if not what:
            return list()
        return what

    def get_urls(self) -> list:
        """ Returns (an ordered) list of URLs """
        return self._keys["urls"]

    def _parse(self, data:str) -> int:
        """ Parse [abc]\n\tLINE*\n ...
        Returns 0 on success, or the error-code.
        """
        urls, url_info, ref_url = list(), list(), dict()
        keys = {
            "@original": dict(),
            "@alt": dict(),
            "urls": urls,
            "url-info": url_info,
            }
        if "\n " in data:
            return 101
        if " \n" in data:
            return 102
        lista = re.split(r"\n(\[[^]]*\])\n", "\n" + data)
        # simpler form:	re.split("\n(\[.*\])\n", data)
        items = [stripped_item(item) for item in lista if stripped_item(item)]
        last = None
        for item in items:
            if len(item) == 2 and isinstance(item[1], list):
                #print(f"ITEM: {item}")
                last = (item[0], ['-'.join(item[1])])
            else:
                assert last, f"Unexpected text: {item}"
                token, alist = last
                assert isinstance(alist, list)
                assert len(alist) == 1
                alt_token = alist[0]
                #print(f"TEXT: {item}", alt_token)
                assert alt_token
                assert token not in keys["@original"], f"Duplicate token: {token}"
                astr = ""
                texts = sorted(item)
                for line in texts:
                    astr += line + "\n"
                    if line.startswith("url ="):
                        url = line[len("url = "):].strip()
                        #print("URL:", url, "; FOR:", alt_token, "!")
                        ref_url[alt_token] = url
                keys["@original"][token] = texts
                keys["@alt"][alt_token] = texts
        # First, remote-origin, then the next
        origin = ref_url.get("remote-origin")
        if origin:
            urls.append(origin)
            url_info.append(("remote-origin", origin))
        for kind in sorted(ref_url):
            if kind == "remote-origin":
                continue
            urls.append(ref_url[kind])
            url_info.append((kind, ref_url[kind]))
        self._keys = keys
        # All ok, return 0
        return 0


def stripped_item(astr:str) -> list:
    """ Strip blanks/ tabs and new-lines """

    def lean_token(astr:str) -> list:
        alist = astr.split(" ")
        res = list()
        for entry in alist:
            if len(entry) > 2 and entry[0] == '"' and entry[-1] == '"':
                res.append(entry[1:-1].strip())
                continue
            res.append(entry)
        return res

    if not astr:
        return ""
    lines = astr.splitlines()
    if len(lines) <= 1 and astr[0] == '[' and astr[-1] == ']':
        token = astr[1:-1]
        return [token, lean_token(token)]
    there = [line.strip(" \t") for line in lines if line.strip(" \t")]
    return there

if __name__ == "__main__":
    main()
