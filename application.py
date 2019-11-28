import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd, pass_strong
# personal touch: checking password strength

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
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    balance = db.execute("SELECT cash FROM users WHERE username=:username", username=session['user_id'])[0]['cash']
    owned = db.execute("SELECT symbol, SUM(shares) FROM bought WHERE user=:username GROUP BY symbol", username=session['user_id'])
    grand_total = 0
    stocks = []
    total = 0
    for stock in owned:
        symbol = stock['symbol']
        if not symbol:
            break
        info = lookup(symbol)
        shares = stock['SUM(shares)']
        if shares == 0:
            break
        price = info['price']
        name = info['name']
        total = shares*price
        grand_total += total
        stocks.append([symbol, name, shares, usd(price), usd(total)])
    grand_total += balance
    return render_template("index.html", cash=usd(balance), stocks=stocks, grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    symbol = request.form.get("symbol").upper()
    info = lookup(symbol)
    if not info:
        return apology("Invalid symbol.")
    shares = request.form.get("shares")
    if not shares:
        return apology("Please enter a positive number of shares.")
    acceptable = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for character in shares:
        if character not in acceptable:
            return apology("Input must be a positive integer.")
    shares = int(shares)
    if shares <= 0:
        return apology("Input must be a positive integer.")
    price = info['price']
    name = info['name']
    total = price*shares
    balance = db.execute("SELECT cash FROM users WHERE username=:username", username=session['user_id'])[0]['cash']
    if total > balance:
        return apology("You don't have enough money.")
    time = datetime.now()
    hist = db.execute("SELECT symbol, shares FROM bought WHERE symbol=:symbol AND user=:username",
                      symbol=symbol, username=session['user_id'])
    if not hist:
        db.execute("INSERT INTO bought (user, symbol, shares, price, time) VALUES (:user, :symbol, :shares, :price, :time)",
                   user=session['user_id'], symbol=symbol, shares=shares, price=price, time=time)
    else:
        hist = hist[0]
        exists = hist['symbol']
        if not exists:
            db.execute("INSERT INTO bought (user, symbol, shares, price, time) VALUES (:user, :symbol, :shares, :price, :time)",
                       user=session['user_id'], symbol=symbol, shares=shares, price=price, time=time)
        else:
            new_shares = hist['shares'] + shares
            db.execute("UPDATE bought SET shares = :shares WHERE user=:user AND symbol=:symbol",
                       shares=new_shares, user=session['user_id'], symbol=symbol)
    db.execute("INSERT INTO history (user, type, shares, symbol, price, time) VALUES (:user, 'buy', :shares, :symbol, :price, :time)",
               user=session['user_id'], shares=shares, symbol=symbol, price=price, time=time)
    db.execute("UPDATE users SET cash = :cash WHERE username=:username", cash=balance - total, username=session['user_id'])
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    data = db.execute("SELECT * FROM history WHERE user=:username", username=session['user_id'])
    stocks = []
    if data != []:
        for item in data:
            symbol = item['symbol']
            price = item['price']
            trans_type = item['type']
            shares = item['shares']
            time = item['time']
            name = lookup(symbol)['name']
            stocks.append([symbol, name, shares, usd(price), trans_type, time])
    return render_template("history.html", stocks=stocks)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    symbol = request.form.get("symbol")
    try:
        info = lookup(symbol)
    except:
        return apology("Invalid symbol.")
    if not info:
        return apology("Invalid symbol.")
    amount = info['price']
    company = info['name'] + " (" + info['symbol'] + ")"
    return render_template("quoted.html", name=company, amount=amount)


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # see what you can sell
    owned = db.execute("SELECT symbol, SUM(shares) FROM bought WHERE user=:username GROUP BY symbol", username=session['user_id'])
    symbols = []
    for stock in owned:
        symbol = stock['symbol']
        if not symbol:
            break
        if stock['SUM(shares)'] != 0:
            symbols.append(symbol)
    if request.method == "GET":
        return render_template("sell.html", symbols=symbols)
    # otherwise, do this stuff for a post request
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")
    if not shares:
        return apology("Please input a positive number of shares.")
    acceptable = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for character in shares:
        if character not in acceptable:
            return apology("Input must be a positive integer.")
    shares = int(shares)
    if shares <= 0:
        return apology("Input must be a positive integer.")
    to_sell = ""
    # can't sell more than you own
    for stock in owned:
        if stock['symbol'] == symbol:
            if stock['SUM(shares)'] < shares:
                return apology("You don't own that many shares.")
            to_sell = stock['symbol']
    if to_sell == "":
        return apology("You don't own that stock.")
    time = datetime.now()
    info = lookup(symbol)
    price = info['price']
    total = price*shares
    # update cash balance
    balance = db.execute("SELECT cash FROM users WHERE username=:username", username=session['user_id'])[0]['cash']
    # update the database differently depending on if you've sold or bought the stock in the past
    hist = db.execute("SELECT symbol, shares FROM bought WHERE symbol=:symbol AND user=:username",
                      symbol=symbol, username=session['user_id'])[0]
    sellhist = db.execute("SELECT symbol, shares FROM sold WHERE symbol=:symbol AND user=:username",
                          symbol=symbol, username=session['user_id'])
    if not sellhist:
        db.execute("INSERT INTO sold (user, symbol, shares, price, time) VALUES (:user, :symbol, :shares, :price, :time)",
                   user=session['user_id'], symbol=to_sell, shares=shares, price=price, time=time)
    else:
        exists = sellhist[0]['symbol']
        if not exists:
            db.execute("INSERT INTO sold (user, symbol, shares, price, time) VALUES (:user, :symbol, :shares, :price, :time)",
                       user=session['user_id'], symbol=to_sell, shares=shares, price=price, time=time)
        else:
            sold_shares = sellhist[0]['shares'] + shares
            db.execute("UPDATE sold SET shares = :shares WHERE user=:user AND symbol=:symbol",
                       shares=sold_shares, user=session['user_id'], symbol=to_sell)
    new_shares = hist['shares'] - shares
    db.execute("UPDATE bought SET shares = :shares WHERE user=:user AND symbol=:symbol",
               shares=new_shares, user=session['user_id'], symbol=to_sell)
    db.execute("INSERT INTO history (user, type, symbol, shares, price, time) VALUES (:user, 'sell', :symbol, :shares, :price, :time)",
               user=session['user_id'], symbol=symbol, shares=shares, price=price, time=time)
    db.execute("UPDATE users SET cash = :cash WHERE username=:username", cash=balance + total, username=session['user_id'])
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
