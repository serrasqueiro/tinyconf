# adate.py  (c)2018  Henrique Moreira (now public, part of 'tconfig')

"""
  Basic money/ accounting classes.

  Compatibility: python 2 and 3.
"""

import datetime


#
# test_adate()
#
def test_adate (args):
  testLeapYears = False
  testModifiedJulianDay = True
  for x in ["good", "bad"]:
    if x=="good":
      dateList = [20180930, 20160229, 20180131, 20180930]
    else:
      dateList = [0, 20180229]
    for xDate in dateList:
      cd1 = CalDate( xDate )
      isOk = cd1.errorCode==0
      print("#", x, "xDate:", xDate, "Is:", cd1.xdate, cd1.to_str())
      if x=="good":
        assert isOk
        last = cd1
      else:
        assert not isOk
  print("Last valid date,", last,
        "; european dotted:", last.to_str( "eu" ),
        "; US:", last.to_str( "" ))
  sd = ShortDate()
  sd.from_caldate( last )
  DoM = sd.day_of_month()
  print("ShortDate():", sd, "(Leap year)" if aDateMaster.is_leap_year( sd.year ) else "(Not leap year)")
  print("Year:", sd.year, "month:", sd.month, "day:", sd.day, "DoM:", DoM)
  if testLeapYears:
    leap19 = [1804, 1808, 1812, 1816, 1820, 1824, 1828, 1832, 1836, 1840, 1844, 1848, 1852, 1856, 1860, 1864, 1868, 1872, 1876, 1880, 1884, 1888, 1892, 1896, 1904, 1908, 1912, 1916, 1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948]
    leap20 = [1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 2032, 2036, 2040, 2044, 2048, 2052, 2056, 2060, 2064, 2068, 2072, 2076, 2080, 2084, 2088, 2092, 2096]
    leapYears = leap19 + leap20
    for year in [2016]:
      for x in range(12):
        m = x+1
        print("Year="+str(year), "Month", m, "days_of_month():", aDateMaster.days_of_month( m, year ))
    for y in range( leapYears[ -1 ] - 1800 + 6 ):
      year = y+1800
      isLeap = year in leapYears
      DoM = aDateMaster.days_of_month( 2, year )
      print("Year", year, "DoM:", DoM, "Leap" if isLeap else ".")
      isOk = isLeap == (DoM>28)
      assert isOk
  if testModifiedJulianDay:
    same = ShortDate()
    for mjd in [58391]:
      isOk = same.from_MJD( mjd )
      theSame = same.match( sd )
      print("MJD", mjd, "is:", same, "=", sd, "OK" if theSame else "NotOk")
      assert theSame
      calcMJD = same.nys_date_to_MJD( 2018, 9, 30 )
      print("calcMJD =", calcMJD)
  if True:
    # Test simple string dates such as '2018-10-13', etc.
    for aStr in ["2018-10-13", "2018-10-31", "2018-10-32", "2018-11-31", "2017-02-29"]:
      sd = ShortDate( aStr )
      isOk = aStr.find( "-32" )<0 and aStr.find( "-11-31" )<0
      isOk = isOk and aStr.find( "-02-29" )<0
      print("ShortDate() of", "'"+aStr+"'", "is:", sd, "Error:", sd.errorCode)
      assert int( isOk==False )==sd.errorCode
  if len( args )>0:
    idx = 10
    y = int( args[ 0 ] )
    if y>=9999:
      sd = ShortDate()
      sd.from_timestamp( y )
      print("ShortDate() from timestamp_ :", y, "sd:", sd)
      z = sd.timestamp()
      print("Timestamp from date at 0:00 :", z)
      assert z-y<86400
      idx = -1
    while idx > 0:
      idx -= 1
      ymd = aDateMaster.calc_easter( y )
      #print("Easter:", ymd)
      sd = ShortDate( ymd )
      calcMJD = sd.nys_date_to_MJD( ymd[0], ymd[1], ymd[2] )
      wd = aDateMaster.week_day( ymd )
      print("Easter:", sd, "MJD:", calcMJD%7, wd, "Sunday" if wd==6 else "?", calcMJD)
      isOk = wd==6
      assert isOk
      y += 1
  return True


#
# CLASS AnyDate
#
class AnyDate:
  def init_anydate (self):
    self.errorCode = 0


  def Master (self):
    return aDateMaster


  def to_string (self, year, month, day, isoFormat):
    assert type( isoFormat )==str
    if isoFormat=="E8601DAw":
      s = "{:04d}-{:02d}-{:02d}".format( year, month, day )
    elif isoFormat=="eu":
      s = "{:02d}.{:02d}.{:04d}".format( day, month, year )
    else:
      s = "{:02d}/{:02d}".format( month, day )
    return s


  def is_ok (self):
    return self.errorCode==0


  def __str__ (self):
    return self.to_str()


  def valid_date (self):
    return aDateMaster.valid_date( self.year, self.month, self.day )


  def nys_date_to_MJD (self, year, month, day):
    y = int( year )
    m = int( month )
    assert type( day )==int
    """ Taken from:	icnames/ntp_analyst.cpp
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
    if y>=1858 and m>=1 and m<=12 and day>=1 and day<=31:
      return 367 * y \
        - int( (7 * (y + int((m + 9) / 12))) / 4 ) \
        - 3 * int((int(int((y + (m - 9) / 7)) / 100) + 1) / 4) \
        + int( 275 * m / 9) \
        + day \
        + 1721028 \
        - 2400000
    return 0


  def compare_days (self, d1, d2):
    if type( d1 )==tuple:
      mjd1 = self.nys_date_to_MJD( d1[ 0 ], d1[ 1 ], d1[ 2 ] )
      mjd2 = self.nys_date_to_MJD( d2[ 0 ], d2[ 1 ], d2[ 2 ] )
    else:
      mjd1 = self.nys_date_to_MJD( d1.year, d1.month, d1.day )
      mjd2 = self.nys_date_to_MJD( d2.year, d2.month, d2.day )
    # Is positive is second date is greater than the first
    return mjd2 - mjd1


  pass


#
# CLASS CalDate
#
class CalDate(AnyDate):
  def __init__ (self, xDate=0):
    self.init_anydate()
    self.firstValidDate = 1970 * 10**4
    self.xdate = 0
    if xDate==0:
      self.errorCode = 2
    else:
      self.errorCode = self.from_xdate( xDate )[ 0 ]==False


  def from_xdate (self, xDate):
    # e.g. 20180930 means the 30th of September
    # from [1], format B8601DAw
    #
    #	where:	[1]  ISO 8601 Basic and Extended Notations
    #
    if type( xDate )==str:
      isOk = len( xDate )>=8
      v = 0
      if isOk:
        try:
          v = int( xDate )
        except:
          pass
      return self.from_xdate( v )
    assert type( xDate )==int
    isOk = xDate>=self.firstValidDate
    year = int( xDate / (10**4) )
    month = int( (xDate-year * 10**4) / 100 )
    day = xDate % 100
    if isOk and self.check_ymd( year, month, day ):
      self.xdate = xDate
      return (True, (year, month, day))
    self.xdate = 0
    return (False, (0, 0, 0))


  def from_short_date (self, shortDate):
    # Returns triplet of (year,month,day)
    tup = None
    if type( shortDate )==str:
      if shortDate.find( '-' )==4:
        tup = self.from_xdate( shortDate.replace( "-", "" ) )
    if not tup:
      tup = self.from_xdate( 0 )
    self.errorCode = tup[ 0 ]==False
    return tup[ 1 ]


  def check_ymd (self, year, month, day):
    try:
      dt = datetime.date( year, month, day )
    except:
      dt = None
    return dt!=None


  def to_str (self, isoFormat="E8601DAw"):
    if self.xdate<=0:
      return "-"
    year = int( self.xdate / (10**4) )
    month = int( (self.xdate-year * 10**4) / 100 )
    day = self.xdate % 100
    return self.to_string( year, month, day, isoFormat )


#
# CLASS ShortDate
#
class ShortDate(AnyDate):
  def __init__ (self, y=0, m=0, d=0, isDayMonth=True):
    self.init_anydate()
    self.year = y
    self.month = y
    self.day = d
    if type( y )==str:
      # Date of format 'YYYY-MM-DD' (see date +%F)
      assert type( m )==int
      isOk = True
      if y.find( "/" )>0:
        spl = y.split( "/" )
        isOk = len( spl )>=2
        if isOk:
          if isDayMonth:
            day = spl[ 0 ]
            month = spl[ 1 ]
          else:
            day = spl[ 1 ]
            month = spl[ 0 ]
          self.year = 0 if len( spl )<=2 else int( spl[ 2 ] )
          self.month = month
          self.day = day
      isOk = len( y )>=10
      if isOk:
        self.errorCode = int( self.from_date( y )==False )
    elif type( y )==int:
      isOk = self.valid_date()
      self.errorCode = int( isOk==False )
    else:
      assert type( y )==tuple
      self.from_date( y )
    pass


  def set_no_date (self):
    self.year = 0
    self.month = 0
    self.day = 0


  def from_caldate (self, calDate):
    if True:
      year = int( calDate.xdate / (10**4) )
      month = int( (calDate.xdate-year * 10**4) / 100 )
      day = calDate.xdate % 100
    self.year = year
    self.month = month
    self.day = day
    return True


  def from_date (self, aStr):
    self.set_no_date()
    if (type( aStr )==list or type( aStr )==tuple) and len( aStr )>=3:
      y = aStr[ 0 ]
      m = aStr[ 1 ]
      d = aStr[ 2 ]
      isOk = type( y )==int and type( m )==int and type( d )==int
      if isOk:
        self.year = y
        self.month = m
        self.day = d
      return self.valid_date()
    else:
      assert type( aStr )==str
      cal = CalDate()
      tuples = cal.from_xdate( aStr.replace( "-", "" ) )
      isOk = tuples[ 0 ]==True
      if isOk:
        return self.from_date( [tuples[ 1 ][ 0 ], tuples[ 1 ][ 1 ], tuples[ 1 ][ 2 ]] )
    return False


  def timestamp (self):
    try:
      ts = int( datetime.datetime( self.year, self.month, self.day ).timestamp() )
    except:
      ts = 0
    if ts<315576000 or ts>6342926400:
      return 0
    return ts

    
  def from_timestamp (self, ts=0):
    self.set_no_date()
    isOk = ts>=315576000	# "1980-01-01 12:00"
    isOk = isOk and ts<=6342926400	# "2170-12-31 12:00"
    if isOk:
      dttm = datetime.datetime.utcfromtimestamp( ts )
      self.year = dttm.year
      self.month = dttm.month
      self.day = dttm.day
    return isOk


  def day_of_month (self):
    return aDateMaster.day_of_month( self )


  def from_MJD (self, mjd):
    assert type( mjd )==int
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


  def match (self, sd):
    return self.year==sd.year and self.month==sd.month and self.day==sd.day


  def to_str (self, isoFormat="E8601DAw"):
    return self.to_string( self.year, self.month, self.day, isoFormat )


#
# CLASS DateMaster
#
class DateMaster:
  def __init__ (self):
    self.monthDuration = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    weekDays = {0:["Mon", "Mo", "Monday"],
              1:["Tue", "Tu", "Tuesday"],
              2:["Wed", "We", "Wednesday"],
              3:["Thu", "Th", "Thursday"],
              4:["Fri", "Fr", "Friday"],
              5:["Sat", "Sa", "Saturday"],
              6:["Sun", "Su", "Sunday"],
              7:["???", "-", "--"]}
    self.hash_weekdays( weekDays )
    self.set_month_abbreviation()
    self.hash_month_names()
    self.mjd = 0
    assert len( self.monthDuration )-1==12


  def set_month_abbreviation (self, strings=None):
    if strings is None:
      self.monthAbbreviation = ("-", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    else:
      aList = strings.split( ";" )
      assert len( aList )==12+1
      self.monthAbbreviation = tuple( aList )
    return self.upper_abbrev()


  def upper_abbrev (self):
    assert len( self.monthAbbreviation )==12+1
    res = []
    for a in self.monthAbbreviation:
      res.append( a.upper() )
    self.monthAbbreviationUp = tuple( res )
    return self.hash_month_names()


  def hash_month_names (self, abbreviationList=None):
    if abbreviationList is None:
      return self.hash_month_names( (self.monthAbbreviation, self.monthAbbreviationUp) )
    assert type( abbreviationList )==tuple or type( abbreviationList )==list
    aDict = {}
    for tups in abbreviationList:
      idx = 0
      for a in tups[ 1: ]:
        idx += 1
        aDict[ a ] = idx
    self.monthDict = aDict
    return True


  def month_name (self, aName):
    assert type( aName )==str
    try:
      m = self.monthDict[ aName ]
    except:
      m = None
    if m is None:
      return 0
    return m


  def hash_weekdays (self, wd):
    assert len( wd )==7+1
    self.weekday = []
    for part in [0, 2]:
      for key, item in wd.items():
        if key>=7:
          break
        self.weekday.append( item[ part ] )
    return True


  def week_day (self, shortDate):
    self.mjd = self.calc_MJD( shortDate )
    return (self.mjd+2) % 7


  def calc_MJD (self, shortDate):
    refDate = ShortDate()
    if type( shortDate )==tuple:
      refDate.from_date( shortDate )
    else:
      refDate.from_date( (shortDate.year, shortDate.month, shortDate.day) )
    self.mjd = refDate.nys_date_to_MJD( refDate.year, refDate.month, refDate.day )
    return self.mjd



  def lang_week_day (self, num):
    assert type( num )==int
    try:
      s = self.weekday[ num ]
    except:
      s = "-"
    return s


  def day_of_month (self, shortDate):
    if type( shortDate )==tuple:
      year = shortDate[ 0 ]
      month = shortDate[ 1 ]
      day = shortDate[ 2 ]
    else:
      year = shortDate.year
      month = shortDate.month
      day = shortDate.day
    if month<1 or month>12 or day<1:
      return -1
    # Returns 1 if it is the first day, 0 if it is the last
    if day==1:
      return 1
    nDays = self.days_of_month( month, year )
    if day==nDays:
      return 0
    if day > nDays:
      return -1
    return day


  def days_of_month (self, month, year=0):
    nDays = 0
    if month>=1 and month<=12:
      nDays = self.monthDuration[ month ]
      if month==2:
        nDays = 28 + int( self.is_leap_year( year ) )
    return nDays


  def is_leap_year (self, year):
    if year==0:
      return False
    assert year>=100
    if year % 4:
      return False
    if year % 100:
      return True
    return (year % 400)==0


  def valid_date (self, year, month, day):
    assert type( year )==int
    assert type( month )==int
    assert type( day )==int
    try:
      aDate = datetime.datetime( year, month, day )
    except ValueError:
      return False
    # Date is valid; considering only >1900
    return year > 1900


  def calc_easter (self, year):
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


  pass


#
# Globals
#
aDateMaster = DateMaster()


#
# Test suite
#
if __name__ == "__main__":
  import sys
  isOk = test_adate( sys.argv[ 1: ] )
  assert isOk
