import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


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
    return render_template("apology.html", top=code, bottom=escape(message)), code


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