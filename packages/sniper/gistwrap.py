#-*- coding: utf-8 -*-
# gistwrap.py  (c)2021  Henrique Moreira

"""
gistwrap, an HTTPS wrapper for gist locations
"""

from htapac2.httpclient2 import HTTPConnection
#from http.client import HTTPConnection
import requests

CONNECT_INFO = ("module", HTTPConnection.__module__,)


def main_test():
    """ Basic test! """
    code = sample()
    print("sample() returned", code)

def sample():
    """ Sample:
	>>> conn = HTTPConnection("gist.github.com")
	>>> page = "/31e19db1dba146e512e4ea39c2c76279.git"
	>>> conn.request("GET", page)
	>>> resp = conn.getresponse()
	>>> http_code = resp.getcode()
	>>> http_code
	301
	>>> data = resp.read()
    """
    for url in (
        "http://gist.github.com/31e19db1dba146e512e4ea39c2c76279.git",
        "https://gist.github.com/31e19db1dba146e512e4ea39c2c76279.git",
        #	... "https://meteo.pt/"
        ):
        print("Checking URL (redirection?) at:", url)
        getter = GistGetter(url)
        where = getter.to_where
        print(f"Redirected ({getter.http_code()}) to: {where}")
        s_to = getter.headers_dict().get('Location')
        print("Original Location (to):", s_to)
        print("--")
    return 0


class Getter():
    """ Generic https URL getter
    """
    _error, _http_code = 0, 0
    _url = ""
    _connection = None
    _headers = []

    def http_code(self) -> int:
        """ Return the last http_code """
        return self._http_code

    def headers_dict(self) -> dict:
        """ Returns the headers dictionary. """
        if not self._headers:
            return {"Location": None}
        return self._headers[0]

    def content_type(self) -> str:
        if len(self._headers) < 2:
            return ""
        return self._headers[1]


class GistGetter(Getter):
    """ GitHub Gist getter
    """
    to_where = ""
    _req = None

    def __init__(self, url:str):
        """ GistGetter wrapper, class init. """
        self._error, self._http_code = 0, 0
        self.to_where = ""
        self._url = url
        if url.startswith(("https://",)):
            req = requests.get(url)
            self._http_code = req.status_code
            self._req = req
            try:
                self.to_where = req.history[-1].url
                self._headers = [req.history[0].headers]
            except IndexError:
                self.to_where = req.url
                self._headers = [req.headers]
        elif url.startswith(("http://",)):
            spl = url.split("://", maxsplit=1)[1]
            domain, page = spl.split("/", maxsplit=1)
            self._connection = HTTPConnection(domain)
            self.get_data("/" + page)

    def response(self):
        """ Returns the response.
        """
        return self._req

    def process_headers(self) -> bool:
        if not self._headers:
            return False
        if len(self._headers) >= 2:
            return False	# No re-processing!
        self._headers.append(what_content_type(self._headers[0]['Content-Type']))
        return True

    def get_data(self, page:str) -> bool:
        """ Connect and get data from (remote) https server """
        self._connection.request("GET", page)
        resp = self._connection.getresponse()
        http_code = resp.getcode()
        self._http_code = http_code
        self._headers = [resp.headers]
        where = resp.headers.get("Location")
        if 300 <= http_code < 400:
            return self._parse_data(where)
        return False

    def _parse_data(self, where:str, data=None) -> bool:
        # pylint: disable=unused-argument
        """ Run data
        """
        self.to_where = ""
        if not where:
            return False
        self.to_where = where
        return True

def what_content_type(content_type:str) -> str:
    """ Returns the content-type from string,
    e.g.
	Content-Type: text/html; charset=utf-8
    is 'utf-8'.
    """
    spl = content_type.split(";")
    for item in spl:
        item = item.strip()
        if item.startswith("charset="):
            cont_type = item.split("=", maxsplit=1)[-1]
            return cont_type.lower()
    return ""

# Main script
if __name__ == "__main__":
    print("Import sniper.gistwrap !")
    main_test()
