# On Track
CS50 Final Project - Karina Halevy, Vanessa Hu, Grace Cen
## Overview
    Our application allows users to track their progress on three goals over the course of a month.
    These goals can be both numerical(number of items) or binary (yes, no).
    Screencast: https://www.youtube.com/watch?v=-VZJRGm6LZg&feature=youtu.be

## Usage: Compiling
Our project lives on the CS50 IDE. To compile, just run ```flask run```.

## Usage:

Setting Up Account:
User is first directed to a login page and must press the register tab of the navbar, located on the upper right corner of the page.
You must follow the parameters provided to create a unique username and password. Then press register.
This will take you to a set goals page, where the user is allowed to enter the names of the 3 goals they want to track and its type (binary or numeric).
Once set, the user will be redirected to the index/homepage, which welcomes the user and displays info on the 3 habits in a carousel.
db
On the index page, each of the 3 pages (cards) of the carousel shows a habit, whether it's logged, Yes/No or numerical amount, and a button to take the user
to the month-calendar page to view the current month calendar for that habit.

Viewing Tracker (Monthly Calendar):
    The user can also always access each habit's month page via the three nav-bar tabs.

    [ Log Data ]
    Once on a month page for a habit, users can use the first form to log data (Yes/No for binary, any non-negative integer for numeric)
    for any month, day, year (each a drop-down menu) since the day they started tracking the habit. Clicking submit will log the data
    and take them back to the calendar page.
    - binary habit: day on calendar is green if completed, red if not, white if not logged
    - numeric habit: number will appear on the corresponding day. If not logged, -- will appear.

    [ Change Month ]
    Under the calendar, there's a drop down menu to select a different month and year for which to display the calendar.

    [ Day View ]
    Below the change month option is another form to select a month, day, year to display the day view for.
    The day display will have a panel at the left with the selected date (chosen in a month calendar page), whether the user logged the data,
    and if so, if it was Yes/No or a numerical amount.

        [ Log Data ]
        Users can also log data for the habit here. The same form as month calendar for logging data will appear.

        [Return to Month View]
        On the right top is a form to select a month and year, to return to the month view for that habit.

        [Change Day]
        On the lower right is another form to select a month, day, year to show the day-view for that date.


Mood Quote Generator: This generates a quote that is fitting for your mood
    After clicking on the Mood Quote Generator tab on the navbar, the user will be able able to press the radio button that corresponds to their mood.
    After pressing submit, users will be redirected to a page where a corresponding quote will be displayed.

## FAQ
    1. What difficulties did you run into?
    When attempting to integrate with Heroku, we realized that real-world sqlite3 was not configured optimally for this purpose.
    This was frustrating because we had meticulously split and stripped sqlite3 execute results using sqlite3 (see original logic in our commit history),
    but we ultimately had to convert back to cs50's SQL.
    Calendar.py

    2. What are some of the biggest challenges you came across?

    2. Why only allow users to track three goals?
    We want users to be able to focus on a few goals and get into the habit of being consistent about them, instead of making the mistake of overestending themselves.
    In terms of implementation, we also did not want to overwhelm our database.

    3. If you had more time, what features would you add?
    We started working on giving users the ability to change the goals that they initially set, in case their goals change after that month is over.
    We would also create a summary section in the binary_month.html and numeric_month.html that displays how many days in the month the user has logged
    that they completed their goal or the average number obtained per days logged in the month.
    We wanted to add a third type of habit, a sliding scale, as well as a mood tracker.

This documentation is to be a user’s manual for your project.
Though the structure of your documentation is entirely up to you,
it should be incredibly clear to the staff how and where, if applicable,
to compile, configure, and use your project. Your documentation should be
at least several paragraphs in length. It should not be necessary for us
to contact you with questions regarding your project after its submission.
Hold our hand with this documentation; be sure to answer in your documentation
any questions that you think we might have while testing your work.

## References
(We have also included in-line references in our source code.)
https://stackoverflow.com/questions/46402022/subtract-hours-and-minutes-from-time
https://stackoverflow.com/questions/26954122/how-can-i-pass-arguments-into-redirecturl-for-of-flask
https://www.programiz.com/python-programming/datetime/strptime
https://docs.python.org/2.5/lib/sqlite3-Cursor-Objects.html
https://docs.python.org/3/library/calendar.html
https://www.geeksforgeeks.org/sql-using-python/
https://cs50.readthedocs.io/heroku/
https://pip.pypa.io/en/stable/installing/
https://www.programiz.com/python-programming/datetime/current-datetime
https://www.w3schools.com/python/python_datetime.asp
https://stackoverflow.com/questions/9481136/how-to-find-number-of-days-in-the-current-month/9481305
CS50 Finance
