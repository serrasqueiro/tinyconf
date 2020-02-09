# adate.test.py  (c)2018, 2020  Henrique Moreira (part of 'tconfig')

"""
  Test

  Compatibility: python 2 and 3.
"""

from adate import aDateMaster, CalDate, ShortDate

# pylint: disable=missing-function-docstring


#
# test_adate()
#
def test_adate(args):
    """
    :param args: System arguments
    :return: True
    """
    testLeapYears = False
    testModifiedJulianDay = True
    isOk = False
    for x in ["good", "bad"]:
        if x == "good":
            dateList = [20180930, 20160229, 20180131, 20180930]
        else:
            dateList = [0, 20180229]
        for xDate in dateList:
            cd1 = CalDate(xDate)
            isOk = cd1.errorCode == 0
            print("#", x, "xDate:", xDate, "Is:", cd1.xdate, cd1.to_str())
            if x == "good":
                assert isOk
                last = cd1
            else:
                assert not isOk
    print("Last valid date,", last,
          "; european dotted:", last.to_str("eu"),
          "; US:", last.to_str(""))
    sd = ShortDate()
    sd.from_caldate(last)
    aDofMonth = sd.day_of_month()
    print("ShortDate():", sd,
          "(Leap year)" if aDateMaster.is_leap_year(sd.year) else "(Not leap year)")
    print("Year:", sd.year, "month:", sd.month, "day:", sd.day, "DoM:", aDofMonth)
    if testLeapYears:
        leap19 = [1804, 1808, 1812, 1816, 1820, 1824, 1828, 1832, 1836, 1840, 1844,
                  1848, 1852, 1856, 1860, 1864, 1868, 1872, 1876, 1880, 1884, 1888,
                  1892, 1896, 1904, 1908, 1912, 1916, 1920, 1924, 1928, 1932, 1936,
                  1940, 1944, 1948]
        leap20 = [1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992,
                  1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 2032, 2036,
                  2040, 2044, 2048, 2052, 2056, 2060, 2064, 2068, 2072, 2076, 2080,
                  2084, 2088, 2092, 2096]
        leapYears = leap19 + leap20
        for year in [2016]:
            for x in range(12):
                m = x+1
                print("Year=" + str(year),
                      "Month", m,
                      "days_of_month():", aDateMaster.days_of_month(m, year))
        for y in range(leapYears[-1] - 1800 + 6):
            year = y+1800
            isLeap = year in leapYears
            aDofMonth = aDateMaster.days_of_month(2, year)
            print("Year", year, "DoM:", aDofMonth, "Leap" if isLeap else ".")
            isOk = isLeap == (aDofMonth > 28)
            assert isOk
    if testModifiedJulianDay:
        same = ShortDate()
        for mjd in [58391]:
            isOk = same.from_MJD(mjd)
            theSame = same.match(sd)
            print("MJD", mjd, "is:", same, "=", sd, "OK" if theSame else "NotOk")
            assert theSame
            calcMJD = same.nys_date_to_MJD(2018, 9, 30)
            print("calcMJD =", calcMJD)
    if isOk:
        # Test simple string dates such as '2018-10-13', etc.
        for aStr, expectedOk in [("2018-10-13", True),
                                 ("2018-10-31", True),
                                 ("2018-10-32", False),
                                 ("2018-11-31", False),
                                 ("2017-02-29", False),
                                 ]:
            sd = ShortDate(aStr)
            isOk = bool(sd.errorCode == 0) == expectedOk
            print("ShortDate() of", "'"+aStr+"'",
                  "is:", sd, "Error:", sd.errorCode,
                  "Test-OK?", isOk)
        y = CalDate(20200229)
        niceOk, (a,b,c) = y.from_xdate( "2018-10-08" )
        assert not niceOk
        assert a==0 and b==0 and c==0
    assert isOk
    if len(args) > 0:
        idx = 10
        y = int(args[0])
        if y >= 9999:
            sd = ShortDate()
            sd.from_timestamp(y)
            print("ShortDate() from timestamp_ :", y, "sd:", sd)
            z = sd.timestamp()
            print("Timestamp from date at 0:00 :", z)
            assert z-y < 86400
            idx = -1
        while idx > 0:
            idx -= 1
            ymd = aDateMaster.calc_easter(y)
            #print("Easter:", ymd)
            sd = ShortDate(ymd)
            calcMJD = sd.nys_date_to_MJD(ymd[0], ymd[1], ymd[2])
            wd = aDateMaster.week_day(ymd)
            print("Easter:", sd, "MJD:", calcMJD%7, wd, "Sunday" if wd == 6 else "?", calcMJD)
            isOk = wd == 6
            assert isOk
            y += 1
    else:
        sd = ShortDate(2020, 2, 29)
        s = str(sd)
        wd = aDateMaster.week_day(sd)
        print("ShortDate(2020, 2, 29): {}, timestamp()={}, lang_week_day({})='{}'".
              format(s, sd.timestamp(), wd, aDateMaster.lang_week_day(wd)))
        assert s=="2020-02-29"
        for m in range(1, 12+1, 1):
            sUp = aDateMaster.monthAbbreviationUp[m]
            y = aDateMaster.month_name(sUp)
            print("#{}={}, name: {}".format(m, y, sUp))
            assert m==y
    return True


#
# Test suite
#
if __name__ == "__main__":
    import sys
    ALL_OK = test_adate(sys.argv[1:])
    assert ALL_OK
