# On Track
CS50 Final Project - Karina Halevy, Vanessa Hu, Grace Cen
## Overview
    Our application allows users to track their progress on three goals over the course of a month.
    These goals can be both numerical(number of items) or binary (yes, no).
    Screencast: https://www.youtube.com/watch?v=-VZJRGm6LZg&feature=youtu.be
    Note: the screencast was done before we successfully deployed to Heroku, so it used ```flask run``` on the CS50 IDE.

## Usage: Compiling
Our project is deployed to Heroku. It can be accessed at https://on-track-cs50.herokuapp.com.

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
    1. What are some difficulties you ran into?
    - When attempting to integrate with Heroku, we realized that real-world sqlite3 was not configured optimally for this purpose.
    This was frustrating because we had meticulously split and stripped sqlite3 execute results using sqlite3 (see original logic in our commit history),
    but we ultimately had to convert back to cs50's SQL.
    - We also had trouble with the program differentiating calendar.py and python's calendar module so we decided to put all of calendar.py's functions into applications.py.
    - We also struggled with the trickle down problems of allowing the user to choose a goal type (binary or numeric).
    Figuring out how to route the nav bar tabs {{goal_1_name}}, {{goal_2_name}}, and {{goal_3_name}} to our binary_month.html or numeric_month.html based on the response of the user.
    - It was difficult to generate a monthly calendar, so we eventually figured out the logic: by creating a table of 4-6 weeks,
    making a list of the date numbers (e.g. 1-30), and pad the front and back of the list with empty spaces so the month would start and end on the accurate days of the week.
    We used dateime and calendar to figure out time and also information about what day of the week a certain month starts in.

    2. Why only allow users to track three goals?
    We want users to be able to focus on a few goals and get into the habit of being consistent about them, instead of making the mistake of overestending themselves.
    In terms of implementation, we also did not want to overwhelm our database.

    3. If you had more time, what features would you add?
    We started working on giving users the ability to change the goals that they initially set, in case their goals change after that month is over.
    We would also create a summary section in the binary_month.html and numeric_month.html that displays how many days in the month the user has logged
    that they completed their goal or the average number obtained per days logged in the month.
    We wanted to add a third type of habit, a sliding scale, as well as a mood tracker.

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
