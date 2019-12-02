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


        return redirect("/goal_1_month")
