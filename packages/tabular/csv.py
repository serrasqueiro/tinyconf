#-*- coding: utf-8 -*-
# csv.py  (c)2020  Henrique Moreira

"""
Parse csv text files
"""

# pylint: disable=no-self-use, missing-function-docstring

_EXCEPT_ENCODINGS = (
    "best-latin",
)


class GenHandle:
    """ Generic handle, with errors """
    _error = 0

    def is_ok(self) -> bool:
        return self._error == 0


class Tabular(GenHandle):
    """ Generic tabular class, for tables """
    _encoding, _enc_try = "UTF-8", ""
    _header = ""
    _num_line = 0
    _separator = ";"
    _col_names = tuple()
    headers, rows = [], []

    def items(self):
        return [item for _, item in self.rows]

    def separator(self):
        return self._separator

    def columns(self):
        return self._col_names[0]

    def column_names(self):
        return self._col_names[1]

    def column_keys(self):
        return self._col_names[2]

    def column_key_names(self):
        return self._col_names[3]

    def renumber(self, new_number=None) -> bool:
        """ Renumber rows """
        if new_number is None:
            new = -len(self.headers)
        else:
            new = int(new_number)
        if not new:
            return False
        idx = 0
        while idx < len(self.rows):
            self.rows[idx][0] += new
            idx += 1
        return True

    def tidy(self, debug=0) -> bool:
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
        is_ok = self._hash_columns()
        if debug > 0:
            print("tidy():", is_ok, "to_del:", to_del)
        return is_ok

    def _hash_columns(self) -> bool:
        """ Hash column names """
        if not self.headers:
            return False
        idx = 0
        _, first = self.headers[0]
        column_names, keying, keys, key_names = first, [], dict(), []
        for name in column_names:
            idx += 1
            key = uncolumn_name(name)
            lo_key = key.lower()
            if lo_key in keys:
                return False
            keys[lo_key] = idx
            keying.append(key)
            key_names.append(lo_key)
        self._col_names = (column_names, keying, keys, key_names)
        return True


class CSV(Tabular):
    """ CSV-text input """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, path=None, header=True, normal_encoding=""):
        """ Constructor """
        assert isinstance(header, bool)
        self._col_names = tuple()
        self.rows = list()
        self._header, self._num_line = "", 0
        self._separator = ","
        if not normal_encoding or normal_encoding in _EXCEPT_ENCODINGS:
            encoder = "UTF-8"
        else:
            encoder = normal_encoding
        self._encoding, self._enc_try = encoder, normal_encoding
        if path:
            code = self._read_file(path, int(header))
        else:
            code = 0
        self._error = code

    def _read_file(self, path, header_lines) -> int:
        """ Read file """
        # pylint: disable=line-too-long
        encoding = self._encoding
        data = None
        if self._enc_try == "best-latin":
            try:
                data = open(path, "r", encoding="ISO-8859-1").read()
            except UnicodeDecodeError:
                data = None
        #print(f"_read_file {path}: header_lines={header_lines}, decode: {encoding} (try: '{self._enc_try})' data?", data is not None)
        if data is None:
            try:
                data = open(path, "r", encoding=encoding).read()
            except UnicodeDecodeError:
                return 101
        if encoding == "UTF-8" and data:
            if 0xfeff == ord(data[0]):
                data = data[1:]
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
            achr = s_line[idx]
            if achr == '"':
                if quoted:
                    quote = process_cell(quote, row)
                quoted = int(quoted == 0)
            else:
                if quoted:
                    quote += achr
                else:
                    if achr == self._separator:
                        if last_ch != '"':
                            a_str = process_cell(a_str, row)
                    else:
                        a_str += achr
            last_ch = achr
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


def uncolumn_name(a_str) -> str:
    u_str = a_str.strip()
    while True:
        new_str = u_str
        u_str = new_str.replace("  ", " ")  # single blank, please
        if u_str == new_str:
            break
    u_str = u_str.replace(" ", "_"). \
        replace("(", ""). \
        replace(")", ""). \
        replace("/", "_")
    return u_str


# Main script
if __name__ == "__main__":
    print("Import tabular.csv !")
