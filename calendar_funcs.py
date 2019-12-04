import calendar
import datetime
import cgi

def display_month_calendar(year, month):
    print(calendar.month(year, month))

def is_leap(year):
    if year % 4 != 0:
        return False
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return True
# need to get month you're looking at. get.request
# need to get get day of week you're looking at.
