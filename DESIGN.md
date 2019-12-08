# On Track

## Tech Stack Overview

### Programs and Programming Languages


### Databases
We have three databases, which we will describe below.
Users stores usernames, user_ids, the hash of the password, as well as the

## Register / Log In
With code from finance.db, the user registers with a unique username and a password that at least one upper case letter, one lower case letter, and one number. Password must also be at least 8 characters long.
Log in also functions like it did in finance.db, checking if the hashes are equal.


## layout.html
We have a Bootstrap nav-bar with three tabs for each goal. It has each goal name since we stored each goal name into session['user_id'] after index 0.


ALERTS!!!!!!!!!!!!!!!!!

## Set Goals
set_goals_html appears right after registering, where the user sets the name and type (binary or numeric) of each of the three habits.
This is done through a form-group, so when the user submits (post), application.py uses request.form.get() to store then update the user in users
with this information: goal_#_name, goal_#_type for 3 goals, as well as the month, day, year integer the user set these goals.
We also store that information so when logging data, the user can't log data before they registered.

## Log In



## Index
Index displays an intro page as well as a Bootstrap carousel, where each picture corresponds to each habit and whether the user logged it or not, and the info if they did.
It does this by iterating through range(1, 4) and accessing the users database and appending to the info list based on whether the habit was done/habit type.
Similarly, it'll display a diff image based on whether the user logged data for that day.

## Goal Display (Month)

## Goal Display (Day)

## Enter Data
    We created two different forms in which our users could enter their data based on the type of goal that they wanted to track: binary or numerical.
    A binary goal is one that you can track by solely saying yes (as in I completed it) or no (I have not completed it).
    The binary goal form is within the binary_day.html file.
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
