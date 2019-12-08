# On Track

## Tech Stack Overview

### Programs and Programming Languages


### Databases
We have three tables in our database tracker.db, which we will describe below.
Users stores usernames, user_ids, the hash of the password, as well as the goal_#_name, goal_#_type for 3 goals.
    It also stores goal_#_year, goal_#_month, goal_#_day.
binary_goals and numeric_goals stores all binary-type and numeric-type entries respectively.
They both have the string-type user (the username linked to users and stored in session);
    the year, month, and day of the entry (stored as integer).
    binary_goals has the integer completed (0 if not, 1 if completed, null if no entry)
    numeric_goals stores under integer amount the integer amount for that habit.

## Register / Log In
With code from finance.db, the user registers with a unique username and a password that at least one upper case letter, one lower case letter, and one number. Password must also be at least 8 characters long.
Log in also functions like it did in finance.db, checking if the hashes are equal.
We have an alert for "Make sure you have already registered!" on login!


## layout.html
Layout.html is the base of all our other HTML pages, and it has the Bootstrap nav-bar with three tabs for each goal.
It has each goal name since we stored each goal name into session['user_id'] after index 0 and pass it in via render_template.
Similarly, the links route to /goal_display/(1, 2, or 3)/{{ year }}/{{ month }}, with current year and month passed in.
However, when the user clicks on the goal tabs, the user is taken to either the binary_month.html or numeric_month.html based on the the type of goal (numeric or binary) the user has determined this particular goal will be.
The fourth link in our nav-bar is our Mood Quote Generator, described below.
## bootstrap features
We added many bootstrap alerts: on the login.html to remind the user to register before having the credentials to login, on the homepage aka index.html to remind the user to log their goals, and
We also added a card in binary_day.html and numeric_day.html and useOther features include a bootstrap carousel

## Set Goals
set_goals_html appears right after registering, where the user sets the name and type (binary or numeric) of each of the three habits.
This is done through a form-group, so when the user submits (post), application.py uses request.form.get() to store then update the user in users
with this information: goal_#_name, goal_#_type for 3 goals, as well as the month, day, year integer the user set these goals.
We also store that information so when logging data, the user can't log data before they registered.


## Index
Index displays some intro text as well as a Bootstrap carousel with 3 images, where each Bootstrap card is a picture-overlay has the habit name, whether the user logged it or not, and the info if they did.
Each card also has a button that takes the user to the monthview, /goal_display/habit#/year/month with year, month variables passed into render_template.
It does this in Python index() by iterating through range(1, 4) for habits 1-3 and accessing the users database and appending to the info list based on whether the habit was done/habit type.
Similarly, it'll display 1 of 2 images based on whether the user logged data for that day, passing a list of length 3 of image links into render_template to display in the carousel on index.html.

## Goal Display (Month)

## Goal Display (Day)


## Enter Data
    We created two different routes in which our users could enter their data based on the type of goal that they wanted to track: binary or numerical.
    For enter_binary_data/<number>/<year>/<month>:
        A binary goal is one that you can track by solely saying yes (as in I completed it) or no (I have not completed it).
        The binary goal form is within the binary_day.html file.
    For enter)numeric_data/<
    A numeric goal is one that you can track by inputting a number. Examples include sleep trackers in which a users inputs the number of hours they get that night or fluid tracker in which a user inputs the number of cups a user has drunk.
    The numeric goal form is within the numeric_day.html file.

## Change Month

## Mood Quote Generator
    The mood quote generator requires the user to input their mood using radio buttons through a form in quotes.html.
    The quotesCalculator function in quotes.py (which we input!) takes that input and returns a song from a list that corresponds to that mood.
    We hard coded lists of three quotes for each mood and implemented the built in python function random so the user has the ability to get different quotes when they use the mood quotes generator tab again and are feeling the same mood.
    The user will then be redirected to the quotes1.html where the quote that the quotesCalculator returns is displayed.


A “design document” for your project in the form of a Markdown file called DESIGN.md
that discusses, technically, how you implemented your project and why you made the design
decisions you did. Your design document should be at least several paragraphs in length.
Whereas your documentation is meant to be a user’s manual, consider your design document
your opportunity to give the staff a technical tour of your project underneath its hood.
