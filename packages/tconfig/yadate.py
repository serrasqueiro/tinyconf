"""
Yet another Date module!

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-docstring, invalid-name, chained-comparison, no-self-use

import sys
import copy
import datetime


def run_tests(ver_num):
    """
    Run basic tests.
    """
    DATE_TUP = (2020, 1, 19, 12, 58, 59)
    dttm = datetime.datetime(*DATE_TUP)
    xDate = GenFDate("now")
    yDate = GenFDate(DATE_TUP)
    zDate = GenFDate()
    zDate.dup(yDate)
    t = str(yDate)
    is_ok = "{}".format(yDate) == "{}".format(zDate)
    ###  is_ok = f"{yDate}" == f"{zDate}"
    assert is_ok
    s = "GenFDate('now')={}, yDate={}".format(xDate, yDate)
    print("Message", s)
    w2 = xDate.get_iso_date(int( dttm.timestamp() ))
    try:
        w = xDate.get_iso_date("2020-01-19 12:58:59")
    except AttributeError:
        w = None
    if w is None:
        w = w2
        print("Low version?", ver_num, "; w:", w)
    w_int = int(w.timestamp())
    other_w = xDate.get_iso_date(w_int)
    print("ISO date: {} = {}".format(w, other_w))
    assert str(w) == t
    assert w == other_w
    assert yDate.date == zDate.date
    try:
        t = zDate.str_date(30200215)
    except ValueError:
        t = None
    assert t is None
    t = zDate.str_date(20200215)
    print("zDate' is: {}, (type: {})".format(t, type(t)))
    return True


class GenFDate():
    """
    GenFDate is a generic functional Date class
    """
    def __init__(self, aDate=None):
        self.date = None
        if aDate is None:
            s = "-"
        elif isinstance(aDate, tuple):
            s = self.date_from(aDate)
        elif isinstance(aDate, str):
            if aDate == "now":
                s = self.conv_datetime(datetime.datetime.now())
            else:
                s = aDate
        else:
            assert False
        self._set_date_time(s)


    def str_date(self, aDate, hasTime=True):
        if aDate is None:
            return "-"
        h, m, s = 0, 0, 0
        if isinstance(aDate, tuple):
            if len(aDate) == 3:
                year, month, day = aDate
            elif len(aDate) == 6:
                year, month, day, h, m, s = aDate
            else:
                assert False
        elif isinstance(aDate, int):
            v = aDate
            if 2000*100*100 <= v < 2200*100*100:
                s = str(v)
            elif v == 0:
                s = "-"
            else:
                raise ValueError
            return s
        else:
            print("Bogus type:", type(aDate))
            assert False
        s = self._shown_date(year, month, day, h, m, s, hasTime)
        return s


    def dup (self, aDate):
        if isinstance(aDate, GenFDate):
            self.date = copy.deepcopy(aDate.date)
        return self


    def date_from(self, tup, hasTime=None):
        if isinstance(tup, (list, tuple)):
            if len(tup) == 3:
                if hasTime is None:
                    hasTime = False
            elif len(tup) == 6:
                if hasTime is None:
                    hasTime = True
            else:
                assert False
            if hasTime:
                year, month, day, h, m, s = tup
                s = self._shown_date(year, month, day, h, m, s, True)
            else:
                year, month, day = tup
                s = self._shown_date(year, month, day, 0, 0, 0, False)
        else:
            assert False
        return s


    def conv_datetime(self, aDtTm, hasTime=True):
        year, month, day = 0, 0, 0
        h, m, s = 0, 0, 0
        if isinstance(aDtTm, datetime.datetime):
            year, month, day = aDtTm.year, aDtTm.month, aDtTm.day
            h, m, s, _ = aDtTm.hour, aDtTm.minute, aDtTm.second, aDtTm.microsecond
        elif isinstance(aDtTm, (tuple, list)):
            if hasTime:
                year, month, day, h, m, s = aDtTm
            else:
                year, month, day = aDtTm
        elif isinstance(aDtTm, int):
            newDateTime = self.conv_from_timestamp(aDtTm)
            assert isinstance(newDateTime, datetime.datetime)
            s = self.conv_datetime(newDateTime)
        else:
            assert False
        if hasTime:
            s = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(year, month, day, h, m, s)
        else:
            s = "{:04}-{:02}-{:02}".format(year, month, day)
        return s


    def conv_from_timestamp(self, aStamp):
        assert isinstance(aStamp, int)
        aDtTm = datetime.datetime.fromtimestamp(aStamp)
        return aDtTm


    def get_iso_date(self, s):
        if isinstance(s, int):
            aDtTm = self.conv_from_timestamp(s)
        elif isinstance(s, str):
            aDtTm = datetime.datetime.fromisoformat(s)
        else:
            assert False
        return aDtTm


    def _shown_date(self, year, month, day, h, m, s, hasTime=True):
        if hasTime:
            s = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(year, month, day, h, m, s)
        else:
            s = "{:04}-{:02}-{:02}".format(year, month, day)
        return s


    def _set_date_time(self, aDate):
        assert isinstance(aDate, str)
        s = aDate
        self.date = s
        return s != "-"


    def __str__(self):
        return self.date


#
# Main script
#
if __name__ == "__main__":
    print("""Import this module.

Follow basic tests.
""")
    run_tests(sys.version_info.major * 100 + sys.version_info.minor)
