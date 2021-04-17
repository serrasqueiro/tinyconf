# (c)2020, 2021  Henrique Moreira
# inspired on https://docs.python.org/3.4/library/html.parser.html#htmlparser-methods

from html.parser import HTMLParser
from html.entities import name2codepoint


def main():
    parser = MyHTMLParser()
    #parser.feed("sample.html")
    feeded(parser, "sample.html")


def feeded(parser, html_path):
    with open(html_path, "r") as fhandle:
        data = fhandle.read()
        parser.feed(data)


def sampler(parser):
    parser.feed('<html><head><title>Test</title></head>'
                '<body><h1>Parse me!</h1></body></html>')


class MyHTMLParser(HTMLParser):
    _details = 0
    _last_tag = ""

    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        self._last_tag = tag
        if self._details:
            for attr in attrs:
                print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data, end='')
        if self._last_tag:
            print("; tagged as:", self._last_tag)
            self._last_tag = ""
        else:
            print("")

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)


class MyHTMLParser_Simple(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)
