#-*- coding: utf-8 -*-
# csv.py  (c)2020  Henrique Moreira

"""
Parse csv text files
"""

# pylint: disable=no-self-use

import sys


def main():
    """ Main script
    """
    code = main_script(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""{__file__} command

Commands are:
    read          Reads csv
""")


def main_script(out, err, args):
    """ Main tests """
    opts = dict()
    if not args:
        return None
    cmd = args[0]
    param = args[1:]
    if cmd == "read":
        for name in param:
            cont = CSV(name, header=True)
            show_content(out, cont, opts)
        return 0
    return None


def show_content(out, cont, opts):
    """ Show table content """
    for row in cont.rows:
        out.write(f"{row}\n")


class Tabular:
    """ Generic tabular class, for tables """
    _encoding = "UTF-8"
    _header = ""
    _num_line = 0
    _separator = ";"
    headers, rows = None, None


class CSV (Tabular):
    """ CSV-text input """
    def __init__(self, path=None, header=True):
        """ Constructor """
        assert isinstance(header, bool)
        self.rows = list()
        self._header, self._num_line = "", 0
        self._separator = ","
        if path:
            self._read_file(path, int(header))

    def _read_file(self, path, header_lines) -> int:
        """ Read file """
        encoding = self._encoding
        data = open(path, "r", encoding=encoding).read()
        self._add_data(data, header_lines)
        return 0

    def _add_data(self, data, header_lines=0) -> int:
        """ Adds data to table
        :param data:
        :return:
        """
        n_line = self._num_line
        headers, payload = list(), list()
        lines = data.strip().splitlines()
        for line in lines:
            n_line += 1
            row = self._add_row(n_line, line)
            if n_line > header_lines:
                payload.append(row)
            else:
                headers.append(row)
        self._num_line = n_line
        self.headers = headers
        self.rows = payload
        return 0

    def _add_row(self, n_line, line) -> list:
        """ Adds and processes a row """
        a_str, quote, quoted = "", "", 0
        last_ch = ""
        idx, row = 0, []
        s_line = line.rstrip()

        def process_cell(a_str, dest) -> str:
            dest.append(a_str)
            return ""

        while idx < len(s_line):
            ch = s_line[idx]
            if ch == '"':
                if quoted:
                    quote = process_cell(quote, row)
                quoted = int(quoted == 0)
            else:
                if quoted:
                    quote += ch
                else:
                    if ch == self._separator:
                        if last_ch != '"':
                            a_str = process_cell(a_str, row)
                    else:
                        a_str += ch
            last_ch = ch
            idx += 1
        if quoted:
            process_cell("?", row)
        else:
            if a_str:
                process_cell(a_str, row)
        return row


# Main script
if __name__ == "__main__":
    main()
