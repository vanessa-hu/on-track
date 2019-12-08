import os
import requests
import urllib.parse
from datetime import datetime, timedelta
from flask import redirect, render_template, request, session
from functools import wraps

# evidence that we did, in fact, try connecting to Heroku with postgresql
postgre = "postgres://hcbgpzlypvdzfn:c3e84575d714ff83f269441d62e00aa6a7041c35b50c41c64d733dc64269276a@ec2-174-129-254-216.compute-1.amazonaws.com:5432/da4grjacno1b4i"

# this function is basically just ripped from CS50 Finance, with a few extra params added in for the layout navbar


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
    return render_template("apology.html", top=code, bottom=escape(message), goal_names=gn, year=int((datetime.now() - timedelta(hours=5)).year), month=int((datetime.now() - timedelta(hours=5)).month)), code


# also ripped from CS50 Finance
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


# ripped from Karina's personal touch from CS50 Finance
def pass_strong(password):
    """Check password strength"""
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


def in_the_future(year, month, day):
    """Check if a date is in the future, based on current time in EST"""
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
    """Check if a date is before the date on which a user registered"""
    if year < start_year:
        return True
    if year == start_year and month < start_month:
        return True
    if year == start_year and month == start_month and day < start_day:
        return True
    return False


def get_postgre():
    """Just good practice using getters and setters instead of straight up ripping variables from other files"""
    # also further evidence that we tried postgresql but failed
    return postgre