import calendar
import datetime
import cgi

def display_month_calendar(year, month):
    print(calendar.month(year, month))

# need to get month you're looking at. get.request
# need to get get day of week you're looking at.
