# On Track

## Tech Stack Overview

### Programs and Programming Languages
Our program uses HTML/CSS, Flask/Python for all our functions and routing, and SQLite3 for our database.
We also have some Javascript linked to Bootstrap.

### Databases
We have three tables in our database tracker.db, which we will describe below.
Users stores usernames, an autoincrementing set of ids, the hash of the password, as well as the goal\_[number]\_name, goal\_[number]\_type for 3 goals.
It also stores goal\_[number]\_year, goal\_[number]\_month, and goal\_[number]\_day.
binary\_goals and numeric_goals stores all binary-type and numeric-type entries respectively.
They both have the string-type user (the username linked to users and stored in session);
the year, month, and day of the entry (stored as integer).
binary_goals has the integer completed (0 if not, 1 if completed, null if no entry)
numeric_goals stores under integer amount the integer amount for that habit.

## Register / Log In
With code from CS50 Finance, the user registers with a unique username and a password that at least one upper case letter, one lower case letter, and one number. Password must also be at least 8 characters long.
Log in also functions like it did in finance.db, checking if the hashes are equal.
We have an alert for "Make sure you have already registered!" on login.


## layout.html
Layout.html is the base of all our other HTML pages, and it has the Bootstrap nav-bar with three tabs for each goal.
It has each goal name since we stored each goal name into session['user\_id'] after index 0 and pass it in via render_template.
Similarly, the links route to /goal_display/(1, 2, or 3)/{{ year }}/{{ month }}, with current year and month passed in.
However, when the user clicks on the goal tabs, the user is taken to either the binary\_month.html or numeric\_month.html based on the the type of goal (numeric or binary) the user has determined this particular goal will be.
The fourth link in our nav-bar is our Mood Quote Generator, described below.

## Bootstrap Features
Bootstrap alerts:
on the login.html to remind the user to register before having the credentials to login, on the homepage aka index.html to remind the user to log their goals, and

Bootstrap cards:
We placed one card in binary\_day.html and numeric\_day.html and used the class="card-img-overlay" to display the date that the user chose to view in day view over it.
We also have the card's caption display the data inserted for that particular day

Bootstrap carousel:
Our carousel, located in index.html, displays 3 images for whether or not each of the 3 goals have been logged and this is explained in the index section below.

## Set Goals
set\_goals.html appears right after registering, where the user sets the name and type (binary or numeric) of each of the three habits.
This is done through a form-group, so when the user submits (post), application.py uses request.form.get() to store then update the user in users
with this information: goal_#_name, goal_#_type for 3 goals, as well as the month, day, year integer the user set these goals.
We also store that information so when logging data, the user can't log data before they registered.


## Index
Index displays some intro text as well as a Bootstrap carousel with 3 images, where each Bootstrap card is a picture-overlay has the habit name, whether the user logged it or not, and the info if they did.
Each card also has a button that takes the user to the monthview, /goal_display/habit#/year/month with year, month variables passed into render_template.
It does this in Python index() by iterating through range(1, 4) for habits 1-3 and accessing the users database and appending to the info list based on whether the habit was done/habit type.
Similarly, it'll display 1 of 2 images based on whether the user logged data for that day, passing a list of length 3 of image links into render_template to display in the carousel on index.html.

## Goal Display (Month)
In binary_month.html, we created an empty 7x4 (for a month that spans 4 week), 7x5(for a month that spans 5 week), and 7x6 (for a month that spans 6 week) html table and used html if statements to choose which to display.
Then we passed in the dates and the data using an if statement in application.py and added padding for the days before the first of that month in the table.
### Timezone Adjustment
We use Python's datetime module to calculate the current date and time for various functions. However, datetime calculates times in UTC, which is 5 hours ahead of EST.
To adjust for this, we use the timedelta module and subtract timedelta(hours=5) to get the current UTC date and time minus five hours. Hence, by default, our app works in EST.


## Enter Data
Users can log data for a habit both from day and month-view, binary or numeric html pages.
Each of these pages has a form that takes in desired month, year, day. Binary pages take Yes/No in a dropdown; numeric pages take numeric input.
We created two different routes in which our users could enter their data based on the type of goal that they wanted to track: binary or numerical.

For enter\_binary\_data/\<number\>/\<year\>/\<month\>:
A binary goal is one that you can track by solely saying yes (as in I completed it) or no (I have not completed it).
We make a form to submit to binary within the binary\_day.html and binary\_month html files.

For enter\_numeric\_data/\<number\>/\<year\>/\<month\>:
A numeric goal is one that you can track by inputting a number. Examples include sleep trackers in which a users inputs the number of hours they get that night or fluid tracker in which a user inputs the number of cups a user has drunk.
The numeric goal form is within the numeric_day.html file.

## Goal Display (Day)
The app route "goal\_display_day/\<number\>" can be accessed from any habit's month-display page.
We have a form that collects desired year, month, and day to stored, and we use .strptime to convert these strings to a date object
to use .weekday() to get the weekday.
There's a list of possible pic backgrounds that we randomly choose using random.choice().
We access the binary\_goals or numeric\_goals table based on the goal\_type, and store the answer into data.
We thus either render binary\_day or numeric\_day.html.
    Both pages have a Bootstrap card on the side with an image, the data overlay on top, and the logged info.
    The left side has a form to switch to month view (/goal\_display route) or to log info.


## Mood Quote Generator
    The mood quote generator requires the user to input their mood using radio buttons through a form in quotes.html.
    The quotesCalculator function in quotes.py (which we input!) takes that input and returns a song from a list that corresponds to that mood.
    We hard coded lists of three quotes for each mood and implemented the built in python function random so the user has the ability to get different quotes when they use the mood quotes generator tab again and are feeling the same mood.
    The user will then be redirected to the quotes1.html where the quote that the quotesCalculator returns is displayed.

## Apology
We modified CS50 Finance's apology function by passing in parameters for year, month, and goal_names.
This is because layout.html requires these parameters on its navigation bar (it needs to display the goal names so the user can view their data).

## Some Comments on Design Choices
We decided to use one goal_display function that passed in the number, year, and month parameters, which saved us a lot of copying compared to if we had had separate display functions for goals 1, 2, and 3.
We also chose to split up the tables as we did so that we had just enough differentiation between binary and numeric goals while not having to repeat things like the user's password or unnecessarily split up different goals.
We chose this design over having separate tables for goal 1, goal 2, and goal 3 because these numberings are arbitrary, and the goal type is more important.
