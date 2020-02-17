# adate.py  (c)2018. 2020  Henrique Moreira (now public, part of 'tconfig')

"""
  Basic money/ accounting classes.

  Compatibility: python 2 and 3.
"""

import datetime
# pylint: disable=invalid-name, pointless-string-statement, missing-function-docstring, no-self-use
# pylint: disable=chained-comparison, attribute-defined-outside-init

#
# Abstract CLASS AnyDate
#
class AnyDate():
    """
    AnyDate abstract class
    """
    def init_anydate(self):
        """
        Initializer.
        :return: void
        """
        self.errorCode = 0
        self.isoFormat = "E8601DAw"


    def to_string(self, year, month, day, isoFormat=None):
        if isoFormat is None:
            isoFmt = self.isoFormat
        else:
            isoFmt = isoFormat
        assert isinstance(isoFmt, str)
        if isoFmt == "E8601DAw":
            s = "{:04d}-{:02d}-{:02d}".format(year, month, day)
        elif isoFmt == "eu":
            s = "{:02d}.{:02d}.{:04d}".format(day, month, year)
        else:
            s = "{:02d}/{:02d}".format(month, day)
        return s


    def is_ok(self):
        return self.errorCode == 0


    def nys_date_to_MJD(self, year, month, day):
        """
        Normative Year Stamp to MJD
        :param year: year
        :param month: month value
        :param day: day of month
        :return: MJD, the Julian Date
        """
        y = int(year)
        m = int(month)
        assert isinstance(day, int)
        """ Taken from:     icnames/ntp_analyst.cpp
        long nys_DateToMjd (int y, int m, int day)
        {
         if ( y>=1858 && m>=1 && m<=12 && day>=1 && day<=31 ) {
            return
                367 * y
                - 7 * (y + (m + 9) / 12) / 4
                - 3 * ((y + (m - 9) / 7) / 100 + 1) / 4
                + 275 * m / 9
                + day
                + 1721028
                - 2400000;
         }
         return 0;
        }
        """
        if y >= 1858 and m >= 1 and m <= 12 and day >= 1 and day <= 31:
            return 367 * y \
              - int( (7 * (y + int((m + 9) / 12))) / 4 ) \
              - 3 * int((int(int((y + (m - 9) / 7)) / 100) + 1) / 4) \
              + int( 275 * m / 9) \
              + day \
              + 1721028 \
              - 2400000
        return 0


    def compare_days(self, d1, d2):
        if isinstance(d1, tuple):
            mjd1 = self.nys_date_to_MJD( d1[ 0 ], d1[ 1 ], d1[ 2 ] )
            mjd2 = self.nys_date_to_MJD( d2[ 0 ], d2[ 1 ], d2[ 2 ] )
        else:
            mjd1 = self.nys_date_to_MJD( d1.year, d1.month, d1.day )
            mjd2 = self.nys_date_to_MJD( d2.year, d2.month, d2.day )
        # Is positive is second date is greater than the first
        return mjd2 - mjd1


#
# CLASS CalDate
#
class CalDate(AnyDate):
    """
    CalDate is a Calendar Date helper class
    """
    def __init__(self, xDate=0):
        self.init_anydate()
        self.firstValidDate = 1970 * 10**4
        self.xdate = 0
        if xDate == 0:
            self.errorCode = 2
        else:
            self.errorCode = not self.from_xdate( xDate )[ 0 ]


    def __str__(self):
        return self.to_str()


    def from_xdate(self, xDate):
        # e.g. 20180930 means the 30th of September
        # from [1], format B8601DAw
        #
        #   where:  [1]  ISO 8601 Basic and Extended Notations
        #
        if isinstance(xDate, str):
            isOk = len(xDate) >= 8
            if isOk:
                try:
                    v = int(xDate)
                except ValueError:
                    v = 0
            return self.from_xdate(v)
        assert isinstance(xDate, int)
        isOk = xDate >= self.firstValidDate
        year = int(xDate / (10**4))
        month = int((xDate-year * 10**4) / 100)
        day = xDate % 100
        if isOk and self.check_ymd( year, month, day ):
            self.xdate = xDate
            return (True, (year, month, day))
        self.xdate = 0
        return (False, (0, 0, 0))


    def from_short_date(self, shortDate):
        # Returns triplet of (year,month,day)
        tup = None
        if isinstance(shortDate, str):
            if shortDate.find('-') == 4:
                tup = self.from_xdate(shortDate.replace( "-", "" ))
        if not tup:
            tup = self.from_xdate( 0 )
        self.errorCode = not tup[ 0 ]
        return tup[ 1 ]


    def check_ymd(self, year, month, day):
        try:
            dt = datetime.date(year, month, day)
        except ValueError:
            dt = None
        return dt is not None


    def to_str(self, isoFormat="E8601DAw"):
        if self.xdate <= 0:
            return "-"
        year = int( self.xdate / (10**4) )
        month = int( (self.xdate-year * 10**4) / 100 )
        day = self.xdate % 100
        return self.to_string(year, month, day, isoFormat)


#
# CLASS ShortDate
#
class ShortDate(AnyDate):
    """
    ShortDate class helper
    """
    def __init__(self, y=0, m=0, d=0, isDayMonth=True):
        self.init_anydate()
        self.year = y
        self.month = m
        self.day = d
        if isinstance(y, str):
            # Date of format 'YYYY-MM-DD' (see date +%F)
            assert isinstance(m, int)
            isOk = True
            if y.find("/") > 0:
                spl = y.split("/")
                isOk = len(spl) >= 2
                if isOk:
                    if isDayMonth:
                        day = spl[ 0 ]
                        month = spl[ 1 ]
                    else:
                        day = spl[ 1 ]
                        month = spl[ 0 ]
                    self.year = 0 if len(spl) <= 2 else int(spl[ 2 ])
                    self.month = month
                    self.day = day
            isOk = len(y) >= 10
            if isOk:
                self.errorCode = int(not self.from_date(y))
        elif isinstance(y, int):
            isOk = self.valid_date()
            self.errorCode = int(not isOk)
        else:
            assert isinstance(y, tuple)
            self.from_date(y)


    def __str__(self):
        return self.to_str()


    def valid_date(self):
        """
        Checks whether date within is valid.
        :return: True iff date is valid.
        """
        return aDateMaster.valid_date(self.year, self.month, self.day)


    def set_no_date(self):
        self.year = 0
        self.month = 0
        self.day = 0


    def from_caldate(self, calDate):
        year = int( calDate.xdate / (10**4) )
        month = int((calDate.xdate-year * 10**4) / 100)
        day = calDate.xdate % 100
        self.year = year
        self.month = month
        self.day = day
        return True


    def from_date(self, aStr):
        self.set_no_date()
        if isinstance(aStr, (list, tuple)) and len(aStr) >= 3:
            y = aStr[ 0 ]
            m = aStr[ 1 ]
            d = aStr[ 2 ]
            isOk = isinstance(y, int) and isinstance(m, int) and isinstance(d, int)
            if isOk:
                self.year = y
                self.month = m
                self.day = d
            return self.valid_date()
        assert isinstance(aStr, str)
        cal = CalDate()
        tuples = cal.from_xdate(aStr.replace( "-", "" ))
        isOk = tuples[ 0 ]
        assert isinstance(isOk, bool)
        if isOk:
            return self.from_date([tuples[ 1 ][ 0 ], tuples[ 1 ][ 1 ], tuples[ 1 ][ 2 ]])
        return False


    def timestamp(self):
        """
        Unix Timestamp
        :return: the Unix timestamp of this date
        """
        try:
            ts = int(datetime.datetime(self.year, self.month, self.day).timestamp())
        except ValueError:
            ts = 0
        if ts < 315576000 or ts > 6342926400:
            return 0
        return ts


    def from_timestamp(self, ts=0):
        """
        Converts from a Unix timestamp
        :param ts:
        :return: True, if entered timestamp is a reasonable date
        """
        self.set_no_date()
        isOk = ts >= 315576000        # "1980-01-01 12:00"
        isOk = isOk and ts <= 6342926400      # "2170-12-31 12:00"
        if isOk:
            dttm = datetime.datetime.utcfromtimestamp(ts)
            self.year = dttm.year
            self.month = dttm.month
            self.day = dttm.day
        return isOk


    def day_of_month(self):
        return aDateMaster.day_of_month(self)


    def from_MJD(self, mjd):
        assert isinstance(mjd, int)
        """
        //C++ code:
        const TK_MJD_TO_J( 2400001 )
        const int J( mjdDay + TK_MJD_TO_J );
        p = J + 68569;
        q = 4*p/146097;
        r = p - (146097*q + 3)/4;
        s = 4000*(r+1)/1461001;
        t = r - 1461*s/4 + 31;
        u = 80*t/2447;
        v = u/11;

        const int Y = 100*(q-49)+s+v;
        const int M = u + 2 - 12*v;
        const int D = t - 2447*u/80;

        year = Y;
        month = M;
        day = D;
        """
        J = mjd + 2400001
        p = J + 68569
        q = int( 4*p / 146097 )
        r = p - int( (146097*q + 3)/4 )
        s = int( 4000*(r+1)/1461001 )
        t = r - int( 1461*s/4 ) + 31
        u = int( 80*t/2447 )
        v = int( u/11 )
        self.year = 100*(q-49)+s+v
        self.month = u + 2 - 12*v
        self.day = t - int( 2447*u/80 )
        #print("from_MJD()", mjd, "is:", self.year, self.month, self.day)
        return True


    def match(self, sd):
        return self.year == sd.year and self.month == sd.month and self.day == sd.day


    def to_str(self, isoFormat="E8601DAw"):
        return self.to_string(self.year, self.month, self.day, isoFormat)


#
# CLASS DateMaster
#
class DateMaster:
    """
    Singleton Date Master!
    """
    def __init__(self):
        """
        Initializer of DateMaster
        """
        self.monthDuration = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        weekDays = {0:["Mon", "Mo", "Monday"],
                    1:["Tue", "Tu", "Tuesday"],
                    2:["Wed", "We", "Wednesday"],
                    3:["Thu", "Th", "Thursday"],
                    4:["Fri", "Fr", "Friday"],
                    5:["Sat", "Sa", "Saturday"],
                    6:["Sun", "Su", "Sunday"],
                    7:["???", "-", "--"]}
        self.monthAbbreviationUp = None
        self.hash_weekdays(weekDays)
        self.set_month_abbreviation()
        self.hash_month_names()
        self.mjd = 0
        assert len(self.monthDuration)-1 == 12


    def set_month_abbreviation(self, strings=None):
        abbr = ("-",
                "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
                )
        if strings is None:
            self.monthAbbreviation = abbr
        else:
            aList = strings.split(";")
            assert len( aList ) == 12+1
            self.monthAbbreviation = tuple(aList)
        return self.upper_abbrev()


    def upper_abbrev(self):
        assert len(self.monthAbbreviation) == 12+1
        res = []
        for m in self.monthAbbreviation:
            res.append(m.upper())
        self.monthAbbreviationUp = tuple(res)
        return self.hash_month_names()


    def hash_month_names(self, abbreviationList=None):
        if abbreviationList is None:
            return self.hash_month_names( (self.monthAbbreviation, self.monthAbbreviationUp) )
        assert isinstance(abbreviationList, (tuple, list))
        aDict = {}
        for tups in abbreviationList:
            idx = 0
            for m in tups[ 1: ]:
                idx += 1
                aDict[m] = idx
        self.monthDict = aDict
        return True


    def month_name(self, aName):
        """
        Converts a string to a month number
        :param aName: month name
        :return: the number of the month, or 0 on error.
        """
        assert isinstance(aName, str)
        try:
            m = self.monthDict[ aName ]
        except KeyError:
            m = None
        if m is None:
            return 0
        return m


    def hash_weekdays(self, week_days_list):
        wd = week_days_list
        assert len(wd) == 7+1
        self.weekday = []
        for part in [0, 2]:
            for key, item in wd.items():
                if key >= 7:
                    break
                self.weekday.append( item[ part ] )
        return True


    def week_day(self, shortDate):
        self.mjd = self.calc_MJD( shortDate )
        return (self.mjd+2) % 7


    def calc_MJD(self, shortDate):
        refDate = ShortDate()
        if isinstance(shortDate, tuple):
            refDate.from_date( shortDate )
        else:
            refDate.from_date( (shortDate.year, shortDate.month, shortDate.day) )
        self.mjd = refDate.nys_date_to_MJD( refDate.year, refDate.month, refDate.day )
        return self.mjd



    def lang_week_day(self, num):
        assert isinstance(num, int)
        try:
            s = self.weekday[ num ]
        except IndexError:
            s = "-"
        return s


    def day_of_month(self, shortDate):
        """
        Day of month of a short date
        :param shortDate: short date
        :return: -1 on error; 1 if this is the first day of that month, or 0 if it is the last
        """
        if isinstance(shortDate, tuple):
            year = shortDate[ 0 ]
            month = shortDate[ 1 ]
            day = shortDate[ 2 ]
        else:
            year = shortDate.year
            month = shortDate.month
            day = shortDate.day
        if month < 1 or month > 12 or day < 1:
            return -1
        # Returns 1 if it is the first day, 0 if it is the last
        if day == 1:
            return 1
        nDays = self.days_of_month( month, year )
        if day == nDays:
            return 0
        if day > nDays:
            return -1
        return day


    def days_of_month(self, month, year=0):
        """
        Days of a Month
        :param month: month number
        :param year: year number
        :return: the number of days for that month
        """
        nDays = 0
        if month >= 1 and month <= 12:
            nDays = self.monthDuration[ month ]
            if month == 2:
                nDays = 28 + int( self.is_leap_year( year ) )
        return nDays


    def is_leap_year(self, year):
        if year == 0:
            return False
        assert year >= 100
        if year % 4:
            return False
        if year % 100:
            return True
        return (year % 400) == 0


    def valid_date(self, year, month, day):
        assert isinstance(year, int)
        assert isinstance(month, int)
        assert isinstance(day, int)
        try:
            aDate = datetime.datetime(year, month, day)
        except ValueError:
            return False
        assert aDate is not None
        # Date is valid; considering only >1900
        return year > 1900


    def calc_easter(self, year):
        """Returns Easter as a date object.
       Devised in 1876 and first appeared in Butcher's Ecclesiastical Handbook.
    """
        a = year % 19
        b = year // 100
        c = year % 100
        d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
        e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
        f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
        month = f // 31
        day = f % 31 + 1
        return (year, month, day)


#
# Globals
#
aDateMaster = DateMaster()


#
# Test suite
#
if __name__ == "__main__":
    print("Import this module!")
