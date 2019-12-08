import os
import requests
import urllib.parse
from datetime import datetime, timedelta
from flask import redirect, render_template, request, session
from functools import wraps

postgre = "postgres://fwqwwrtldorygc:4fdaacff36970c52281ab1028a3533d37c6ce75e149675a10881b382aef234e2@ec2-107-20-239-47.compute-1.amazonaws.com:5432/dfndjppmhgdfs7"
goal_names = ["", "", ""]
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    try:
        gn = session["user_id"][1:]
    except:
        gn = ["", "", ""]
    return render_template("apology.html", top=code, bottom=escape(message), goal_names = gn, year = int((datetime.now() - timedelta(hours=5)).year), month = int((datetime.now() - timedelta(hours=5)).month)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def pass_strong(password):
    lower_case = "abcdefghijklmnopqrstuvwxyz"
    upper_case = lower_case.upper()
    numbers = "1234567890"
    contains_lower = False
    contains_upper = False
    contains_number = False
    if len(password) < 8:
        return False
    for letter in lower_case:
        if letter in password:
            contains_lower = True
            break
    for letter in upper_case:
        if letter in password:
            contains_upper = True
            break
    for number in numbers:
        if number in password:
            contains_number = True
            break
    if not contains_lower:
        return False
    if not contains_upper:
        return False
    if not contains_number:
        return False
    return True

def get_goal_names():
    return goal_names

def set_goal_names(item1, item2, item3):
    goal_names[0] = item1
    goal_names[1] = item2
    goal_names[2] = item3

def in_the_future(year, month, day):
    now = datetime.now() - timedelta(hours=5)
    this_year = now.year
    this_month = now.month
    this_day = now.day
    if year > this_year:
        return True
    if year == this_year and month > this_month:
        return True
    if year == this_year and month == this_month and day > this_day:
        return True
    return False

def before_start(year, month, day, start_year, start_month, start_day):
    if year < start_year:
        return True
    if year == start_year and month < start_month:
        return True
    if year == start_year and month == start_month and day < start_day:
        return True
    return False

def get_postgre():
    return postgre
