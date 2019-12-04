import calendar
import datetime
import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')
y = int(input(request.args.get("/enter_desired_month")))
m = int(input("Input the month : "))
print(calendar.month(y, m))
# need to get month you're looking at. get.request
# need to get get day of week you're looking at.
