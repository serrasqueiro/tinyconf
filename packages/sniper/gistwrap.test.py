#-*- coding: utf-8 -*-
# gistwrap.test.py  (c)2021  Henrique Moreira

"""
Tests gistwrap!
"""

import sys
import requests
from sniper.gistwrap import GistGetter

DEBUG = 0


def main():
    """ Main script """
    code = main_test(sys.argv[1:])
    is_ok = code == 0
    if not is_ok:
        print(f"main_test() returned non-zero: {code}")
        sys.exit(1)
    sys.exit(0)

def main_test(args: list) -> int:
    """ Basic test! """
    errors = 0
    if not args:
        params = ["pt"]
    else:
        params = args
    for param in params:
        url = "https://meteo.pt" if param in ("pt",) else param
        print("Checking URL (redirection?) at:", url)
        try:
            getter = GistGetter(url)
        except requests.exceptions.SSLError:
            getter = None
        if getter is None:
            print("SSL error, skipped:", url)
            errors += 1
            continue
        where = getter.to_where
        print(f"Redirected ({getter.http_code()}) to: {where}")
        s_to = getter.headers_dict().get('Location')
        print("Original Location (to):", s_to)
        print("--")
        getter.process_headers()	# Only needed if content_type() is called
        cont_type = getter.content_type()
        if DEBUG > 0:
            show_content(getter.response(), getter.headers_dict(), cont_type)
    return errors

def show_content(resp, hdrs:dict, cont_type, encoding=""):
    """ Debug, show headers and HTML content.
    cont_type is empty if you do not see any 'Content-Type: ... ; charset=utf-8'
    """
    print("RESPONSE:\n")
    heads = list()
    for hdr in sorted(hdrs):
        shown = hdrs[hdr]
        shown = (shown[:60] + " (...)") if len(shown) > 60-3 else shown
        heads.append(f"{hdr}: {shown}")
    print("\n".join(heads))
    print("+--+--+")
    if not cont_type:
        cont_type = "unknown"
    print(f"PAYLOAD (content-type={cont_type}):\n")
    # Usually content-type is UTF-8
    if not encoding:
        encoding = 'utf-8'
    data = resp.content.decode(cont_type if cont_type else encoding)
    lines = data.strip().splitlines()
    for line in lines:
        print(line)

# Main script
if __name__ == "__main__":
    main()
