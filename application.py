import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd, pass_strong

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
connection = sqlite3.connect("tracker.db")
db = connection.cursor()

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    return apology("to do")

@app.route("/enter_data_1", methods=["GET", "POST"])
@login_required
def enter_data_1():
    if request.method == "GET":
        return render_template("enter_data_1.html")
    else:
        didIt = lookup(request.form.get("tracker"))

        # if no answer
        if didIt == None:
            return apology("Must return an answer!")


        # get date info
        now = datetime.datetime.now()
        y = now.year
        m = now.month
        d = now.day
        if db.execute("SELECT username, year, month, day FROM binary_goals WHERE u = :u AND y = :y AND m = :m AND d = :d", u = session['user_id'], y = y, m = m, d = d) == None:
            db.execute("INSERT INTO binary_goals (username, year, month, day) VALUES (:u, :y, :m, :d)",
                u = session['user_id'], y = y, m = m, d = d)
        else:
            # what should we display? just override prev entry or??? can only view calendar history if we log it or no?
            pass


        return render_template("goal_1_month.html")


@app.route("/goal2", methods=["GET", "POST"])
@login_required
def goal2():
    if request.method == "GET":
        return apology("to do")
    return apology("to do")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
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
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/goal3", methods=["GET", "POST"])
@login_required
def goal3():
    if request.method == "GET":
        return apology("to do")
    return apology("to do")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    # by default, it'll do the rest of the stuff if given a post request
    name = request.form.get('username')
    # check if username is taken
    taken = db.execute("SELECT COUNT(username) FROM users WHERE username=:username", username=name)
    if taken[0]['COUNT(username)'] == 1:
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
    # personal touch: check password strength
    if not pass_strong(password):
        return apology("Password must contain at least one upper case letter, one lower case letter, and one number. Password must also be at least 8 characters long.")
    pass_hash = generate_password_hash(password)
    # hash the password and add the account into the user database
    db.execute("INSERT INTO users (username, hash) VALUES (:username, :pass_hash)", username=name, pass_hash=pass_hash)
    # log the user in
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
    session["user_id"] = rows[0]["username"]
    return redirect("/")


@app.route("/enter", methods=["GET", "POST"])
@login_required
def enter():
    """Sell shares of stock"""
    # see what you can sell
    if request.method == "GET":
        return apology("to do")
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)