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
    opts = {"debug": 0,
            "verbose": 0,
            }
    if not args:
        return None
    cmd = args[0]
    param = args[1:]
    while param and param[0].startswith("-"):
        if param[0].startswith("-v"):
            opts["verbose"] += param[0].count("v")
            del param[0]
            continue
        return None
    if cmd == "read":
        for name in param:
            cont = CSV(name, header=True)
            cont.tidy()
            cont.renumber()
            show_content(out, cont, opts)
        return 0
    return None


def show_content(out, cont, opts):
    """ Show table content """
    verbose = opts["verbose"]
    if cont.headers:
        there = [cont.separator().join(listed) for _, listed in cont.headers]
        shown = "\n".join(there)
        mark = "=" * len(there[0])
        if verbose > 0:
            print(f"{shown}\n{mark}")
    for row in cont.rows:
        n_line, listed = row
        if verbose > 0:
            out.write(f"#{n_line}: {listed}\n")
        else:
            r_line = f"{listed}"
            r_line = r_line[1:-1]
            out.write(f"{r_line}\n")


class Tabular:
    """ Generic tabular class, for tables """
    _encoding = "UTF-8"
    _header = ""
    _num_line = 0
    _separator = ";"
    headers, rows = None, None

    def separator(self):
        return self._separator


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

    def renumber(self, new_number=None) -> bool:
        """ Renumber rows """
        if new_number == None:
            new = -len(self.headers)
        else:
            new = int(new_number)
        if not new:
            return False
        idx = 0
        for row in self.rows:
            self.rows[idx][0] += new
            idx += 1
        return True

    def tidy(self):
        """ Tidy table """
        # Removes last empty lines
        to_del, idx = [], len(self.rows)
        for _, item in self.rows[::-1]:
            idx -= 1
            if not is_empty(item):
                break
            to_del.append(idx)
        for a_del in to_del:
            del self.rows[a_del]

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
        lines = data.strip(" ").splitlines()
        for line in lines:
            n_line += 1
            row = self._add_row(n_line, self.line_string_preprocess(line))
            if n_line > header_lines:
                payload.append(row)
            else:
                headers.append(row)
        self._num_line = n_line
        self.headers = headers
        self.rows = payload
        return 0

    def _add_row(self, n_line, s_line) -> list:
        """ Adds and processes a row """
        a_str, quote, quoted = "", "", 0
        last_ch = ""
        idx, row = 0, []

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
        return [n_line, row]

    def line_string_preprocess(self, s_line) -> str:
        return s_line.rstrip()


def is_empty(obj) -> bool:
    return not obj


# Main script
if __name__ == "__main__":
    main()
