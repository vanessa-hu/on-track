import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from helpers import *
import calendar
from quotes import quotesCalculator
import random
# citation: https://stackoverflow.com/questions/46402022/subtract-hours-and-minutes-from-time

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# connect to database
db = SQL("sqlite:///tracker.db")


@app.route("/")
@login_required
def index():
    now = datetime.now() - timedelta(hours=5)
    year = int(now.year)
    month = int(now.month)
    day = int(now.day)
    info = [] # 3 elements to describe info about each habit on this day
    images = [] # 3 pic sources for either logged or not logged
    logged_pic = "https://images.unsplash.com/photo-1456071950267-1b8deae9e997?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2300&q=80"
    not_logged_pic = "https://images.unsplash.com/photo-1486895756674-b48b9b2eacf3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1500&q=80"
    gn = []
    for i in range(1, 4):
        goal_info = db.execute("SELECT * FROM users WHERE username = :u", u=session['user_id'][0])[0]
        goal_name = goal_info["goal_" + str(i) + "_name"]
        goal_type = goal_info["goal_" + str(i) + "_type"]
        if not goal_name:
            gn.append("")
        else:
            gn.append(goal_name)
        # label if goal_type is binary, checks completed field. 0 is no, 1 is yes
        if goal_type == "binary":
            x = db.execute("SELECT completed FROM binary_goals WHERE user=:username AND goal_name=:goal_name AND year=:year AND month=:month AND day=:day",
                        username=session['user_id'][0], goal_name=goal_name, year=year, month=month, day=day)
            if len(x) == 0:
                text = "Completed Today?\n Not Logged"
                images.append(not_logged_pic)
            elif int(x[0]['completed']) == 1:
                text = "Completed Today?\n Yes"
                images.append(logged_pic)
            else:
                text = "Completed Today?\n No"
                images.append(logged_pic)

        else:  # label if goal_type is numeric
            var = db.execute("SELECT * FROM numeric_goals WHERE user=:username AND goal_name=:goal_name AND year=:year AND month=:month AND day=:day",
                            username=session['user_id'][0], goal_name=goal_name, year=year, month=month, day=day)
            if len(var) == 0:
                text = "Num Achieved: Not Logged"
                images.append(not_logged_pic)
            else:
                comp = int(var[0]['amount']) # checks amount field in var, stores in comp
                text = "Num Achieved: " + str(comp)
                images.append(logged_pic)

        info.append(text)
    return render_template("index.html", goal_names=gn, year=year, month=month, info=info, images = images)

# citation: https://stackoverflow.com/questions/26954122/how-can-i-pass-arguments-into-redirecturl-for-of-flask
@app.route("/goal_display/<number>/<year>/<month>", methods = ["GET", "POST"])
@login_required
# default goal_display is current time, at est. takes in form input if posted
def goal_display(number, year = (datetime.now() - timedelta(hours=5)).year, month = (datetime.now() - timedelta(hours=5)).month):
    if request.method == "POST":
        year = request.form.get("desired_year")
        month = request.form.get("desired_month")
    number = int(number)
    if type(year) == list:
        year = int(year[0])
    else:
        year = int(year)
    month = int(month)
    goal_info = db.execute("SELECT * FROM users WHERE username = :u", u=session['user_id'][0])[0]
    goal_name = goal_info["goal_" + str(number) + "_name"]
    goal_type = goal_info["goal_" + str(number) + "_type"]

    started = int(goal_info["goal_" + str(number) + "_year"])
    weekday_num, num_days = calendar.monthrange(year, month)  # zero is monday
    num_weeks = 5

    if weekday_num == 6 and num_days == 28:
        num_weeks = 4
    elif num_days == 31 and (weekday_num == 4 or weekday_num == 5):        # first day is fri/sat, 31 day month
        num_weeks = 6
    elif num_days == 30 and weekday_num == 5:        # first day is fri/sat, 31 day month
        num_weeks = 6

    if weekday_num == 6: #if it's Sunday, start populating from Sunday
        n = 0
    else:
        n = weekday_num + 1
    # spaces before month starts up until 1st weekday, backpad is empty space as well
    front_pad = [" " for i in range(n)]
    back_pad = [" " for i in range(num_weeks*7 - len(front_pad) - num_days)]
    dates = front_pad + [i for i in range(1, 1 + num_days)] + back_pad
    data = []
    if goal_type == "binary":
        for i in range(len(dates)):
            if dates[i] == " ":
                data.append(2)
            else:
                var = db.execute("SELECT * FROM binary_goals WHERE user=:username AND goal_name=:goal_name AND year=:year AND month=:month AND day=:day",
                username=session['user_id'][0], goal_name=goal_name, year=year, month=month, day=dates[i])
                if len(var) == 0:
                    data.append(2)
                else:
                    comp = int(var[0]['completed'])
                    data.append(comp)
    else:
        for i in range(len(dates)):
            if dates[i] == " ":
                data.append(" ")
            else:

                var = db.execute("SELECT * FROM numeric_goals WHERE user=:username AND goal_name=:goal_name AND year=:year AND month=:month AND day=:day",
                username=session['user_id'][0], goal_name=goal_name, year=year, month=month, day=dates[i])
                if len(var) == 0:
                    data.append("--")
                else:
                    comp = int(var[0]['amount'])
                    data.append(comp)
    if goal_type == "binary":
        years = [i for i in range(started, year + 1)]
        return render_template("binary_month.html", month=month, year=year, name=goal_name, data=data, dates=dates, num_weeks=num_weeks, goal_names=session["user_id"][1:], number=number, years=years)
    years = [i for i in range(started, year+1)]
    return render_template("numeric_month.html", month=month, year=year, years = years, name = goal_name, data = data, dates = dates, num_weeks = num_weeks, goal_names = session["user_id"][1:], number = number)

@app.route("/goal_display_day/<number>", methods = ["POST"])
@login_required
def goal_display_day(number):
    year = request.form.get("desired_year")
    month = request.form.get("desired_month")
    day = request.form.get("desired_day")

    # citation: https://www.programiz.com/python-programming/datetime/strptime
    day_of_week = datetime.strptime(month + "/" + day + "/" + year, '%m/%d/%Y').weekday()

    number = int(number)
    year = int(year)
    month = int(month)
    day = int(day)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_text = days[day_of_week] #gets header name
    goal_info = db.execute("SELECT * FROM users WHERE username = :u", u=session['user_id'][0])[0]
    goal_name = goal_info["goal_" + str(number) + "_name"]
    goal_type = goal_info["goal_" + str(number) + "_type"]

    started = goal_info["goal_" + str(number) + "_year"]
    weekday_num, num_days = calendar.monthrange(year, month)  # zero is monday
    years = [i for i in range(started, year + 1)]
    data = ""
    pics = ["https://images.unsplash.com/photo-1564510714747-69c3bc1fab41?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1500&q=80",
    "https://images.unsplash.com/photo-1524678714210-9917a6c619c2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60", "https://images.unsplash.com/photo-1473181488821-2d23949a045a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1500&q=80"]
    pic = random.choice(pics)
    if goal_type == "binary":
        x = db.execute("SELECT completed FROM binary_goals WHERE user=:username AND goal_name=:goal_name AND year=:year AND month=:month AND day=:day",
                     username=session['user_id'][0], goal_name=goal_name, year=year, month=month, day=day)
        label = "Completed Today?"
        if len(x) == 0:
            data = "Not Logged"
        elif int(x[0]['completed']) == 1:
            data = "Yes"
        else:
            data = "No"
        return render_template("binary_day.html", month=month, year=year, day=day, day_text=day_text, name=goal_name, label=label, data=data, goal_names=session["user_id"][1:], number=number, years=years, pic = pic)

    else:

        label = "Amount Achieved"
        var = db.execute("SELECT * FROM numeric_goals WHERE user=:username AND goal_name=:goal_name AND year=:year AND month=:month AND day=:day",
                        username=session['user_id'][0], goal_name=goal_name, year=year, month=month, day=day)
        if len(var) == 0:
            data = "Not Logged"
        else:
            comp = int(var[0]['amount'])
            data = str(comp)

    return render_template("numeric_day.html", month=month, year=year, day=day, day_text=day_text, name=goal_name, label=label, data=data, goal_names=session["user_id"][1:], number=number, years=years, pic = pic)

@app.route("/enter_binary_data/<number>/<year>/<month>", methods=["POST"])
@login_required
def enter_binary_data(number, year, month):
    number = int(number)
    month = int(request.form.get("desired_month"))  # gives int 1-12
    day = int(request.form.get("desired_day"))  # gives int 1-31
    year = int(request.form.get("desired_year"))
    didIt = int(request.form.get("binary_tracker"))  # will be Yes 1, or No 0

    # if no answer
    if didIt == None or month == None or year == None:
        return apology("Must fill in all fields!")
    weekday_num, num_days = calendar.monthrange(year, month)  # 0-6 is Mon-Sun

    if day > num_days:
        return apology("Invalid day for this month.")
    if in_the_future(year, month, day):
        return apology("Can't enter data for the future.")
    date_check = db.execute("SELECT * FROM users WHERE username=:username",
                                username=session['user_id'][0])[0]
    # print(date_check)
    year_check = int(date_check['goal_' + str(number) + '_year'])
    month_check = int(date_check['goal_' + str(number) + '_month'])
    day_check = int(date_check['goal_' + str(number) + '_day'])
    gn = date_check['goal_' + str(number) + '_name']
    # print(year_check, month_check, day_check)
    # print(year, month, day)
    inval = before_start(year, month, day, year_check, month_check, day_check)
    if inval:
        return apology("You started tracking this goal after this date.")
    # get date info
    exists = db.execute("SELECT user, goal_name, year, month, day FROM binary_goals WHERE user = :u AND goal_name = :gn AND year = :y AND month = :m AND day = :d",
                       u=session['user_id'][0], gn=gn, y=year, m=month, d=day)
    if len(exists) == 0:
        db.execute("INSERT INTO binary_goals (user, goal_name, year, month, day, completed) VALUES (:u, :g, :y, :m, :d, :c)",
                    u=session['user_id'][0], g=gn, y=year, m=month, d=day, c=didIt)
    else:
        db.execute("UPDATE binary_goals SET completed = :c WHERE user = :u AND goal_name = :g AND year = :year AND month = :month AND day = :day",
                   c=didIt, u=session['user_id'][0], g=gn, year=year, month=month, day=day)
    if int(number) == 1:
        return redirect("/goal_display/1/" + str(year) + "/" + str(month))
    if int(number) == 2:
        return redirect("/goal_display/2/" + str(year) + "/" + str(month))
    else:
        return redirect("/goal_display/3/" + str(year) + "/" + str(month))


@app.route("/enter_numeric_data/<number>/<year>/<month>", methods=["POST"])
@login_required
def enter_numeric_data(number, year, month):
    number = int(number)
    month = int(request.form.get("desired_month"))  # gives int 1-12
    day = int(request.form.get("desired_day"))  # gives int 1-31
    year = int(request.form.get("desired_year"))
    value = int(request.form.get("numeric_tracker"))  # will be a number

    # if no answer
    if value == None or month == None or year == None:
        return apology("Must fill in all fields!")
    weekday_num, num_days = calendar.monthrange(year, month)  # 0-6 is Mon-Sun

    if day > num_days:
        return apology("Invalid day for this month.")
    if in_the_future(year, month, day):
        return apology("Can't enter data for the future.")
    date_check = db.execute("SELECT * FROM users WHERE username=:username",
                                username=session['user_id'][0])[0]
    # print(date_check)
    year_check = int(date_check['goal_' + str(number) + '_year'])
    month_check = int(date_check['goal_' + str(number) + '_month'])
    day_check = int(date_check['goal_' + str(number) + '_day'])
    gn = date_check['goal_'+str(number) + '_name']
    inval = before_start(year, month, day, year_check, month_check, day_check)
    if inval:
        return apology("You started tracking this goal after this date.")
    # get date info
    exists = db.execute("SELECT user, goal_name, year, month, day FROM numeric_goals WHERE user = :u AND goal_name = :gn AND year = :y AND month = :m AND day = :d",
                        u=session['user_id'][0], gn=gn, y=year, m=month, d=day)
    if len(exists) == 0:
        db.execute("INSERT INTO numeric_goals (user, goal_name, year, month, day, amount) VALUES (:u, :g, :y, :m, :d, :c)",
                   u=session['user_id'][0], g=gn, y=year, m=month, d=day, c=value)
    else:
        db.execute("UPDATE numeric_goals SET amount = :c WHERE user = :u AND goal_name = :g AND year = :year AND month = :month AND day = :day",
                   c=value, u=session['user_id'][0], g=gn, year=year, month=month, day=day)
    if int(number) == 1:
        return redirect("/goal_display/1/" + str(year) + "/" + str(month))
    if int(number) == 2:
        return redirect("/goal_display/2/" + str(year) + "/" + str(month))
    else:
        return redirect("/goal_display/3/" + str(year) + "/" + str(month))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if rows == []:
            return apology("invalid username and/or password", 403)
        pass_hash = rows[0]["password"]
        if not check_password_hash(pass_hash, request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = [request.form.get("username")]
        goal_info = db.execute("SELECT * FROM users WHERE username = :u", u=session['user_id'][0])[0]
        goal_1_name = goal_info['goal_1_name']
        goal_2_name = goal_info['goal_2_name']
        goal_3_name = goal_info['goal_3_name']
        session["user_id"] = [session["user_id"][0]] + [goal_1_name, goal_2_name, goal_3_name]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
# citation: https://docs.python.org/2.5/lib/sqlite3-Cursor-Objects.html
def register():
    if request.method == "GET":
        return render_template('register.html')
    # by default, it'll do the rest of the stuff if given a post request
    name = request.form.get('username')
    # check if username is taken
    taken = int(db.execute("SELECT COUNT(username) FROM users WHERE username=:username", username=name)[0]['COUNT(username)'])
    if taken != 0:
        return apology("Username is already taken.")
    # check if username is blank
    if not name:
        return apology("Username cannot be blank.")
    password = request.form.get('password')
    # check if you enter a password
    if not password:
        return apology("Please enter a password.")
    confirmation = request.form.get('confirmation')
    # need to confirm password
    if not confirmation:
        return apology("Please confirm your password.")
    # check that passwords match
    if password != confirmation:
        return apology("Passwords do not match.")
    if not pass_strong(password):
        return apology("Password must contain at least one upper case letter, one lower case letter, and one number. Password must also be at least 8 characters long.")
    pass_hash = generate_password_hash(password)
    # hash the password and add the account into the user database
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password);", username=name, password=pass_hash)
    # log the user in
    session["user_id"] = [name]
    return redirect("/set_goals")


@app.route("/set_goals", methods=["GET", "POST"])
@login_required
def set_goals():
    if request.method == "GET":
        return render_template("set_goals.html", goal_names=session["user_id"][1:])
    goal_1_name = request.form.get("goal_1_name")
    goal_2_name = request.form.get("goal_2_name")
    goal_3_name = request.form.get("goal_3_name")
    if not goal_1_name or not goal_2_name or not goal_3_name:
        return apology("goal name cannot be blank")
    if goal_1_name.lower() == goal_2_name.lower() or goal_2_name.lower() == goal_3_name.lower() or goal_1_name.lower() == goal_3_name.lower():
        return apology("No two goals can be the same. Click \"Set Goals\" on the upper left to try again.")
    goal_1_type = request.form.get("goal_1_type")
    goal_2_type = request.form.get("goal_2_type")
    goal_3_type = request.form.get("goal_3_type")

    now = datetime.now() - timedelta(hours=5)
    year = now.year
    month = now.month
    day = now.day
    db.execute('''UPDATE users SET goal_1_name=:name1, goal_1_type=:type1, goal_1_year=:year1, goal_1_month=:month1, goal_1_day=:day1,
    goal_2_name=:name2, goal_2_type=:type2, goal_2_year=:year2, goal_2_month=:month2, goal_2_day=:day2,
    goal_3_name=:name3, goal_3_type=:type3, goal_3_year=:year3, goal_3_month=:month3, goal_3_day=:day3
    WHERE username=:username;
    ''',
        name1=goal_1_name, type1=goal_1_type, year1=year, month1=month, day1=day,
        name2=goal_2_name, type2=goal_2_type, year2=year, month2=month, day2=day,
        name3=goal_3_name, type3=goal_3_type, year3=year, month3=month, day3=day, username=session['user_id'][0])
    session["user_id"] = [session["user_id"][0]] + [goal_1_name, goal_2_name, goal_3_name]
    return redirect("/")


@app.route("/quotes", methods=["GET", "POST"])
@login_required
def new_quotes():

    if request.method == "GET":
        return render_template('quotes.html', goal_names=session['user_id'][1:])
    else:
        mood = request.form.get('mood')
        quote = quotesCalculator(mood)

        return render_template('quotes1.html', mood=mood, quote=quote, goal_names=session['user_id'][1:])


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

