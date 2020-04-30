import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp
from flask_session import Session


from helpers import apology

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///contact.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/graphs", methods=["GET", "POST"])
def graphs():
    if request.method == "GET":
        return render_template("graphs.html")
    else:
        graph = request.form.get("graphs")
        if graph == "democrat":
            return render_template("/dem.html")
        if graph == "republican":
            return render_template("/rep.html")
        if graph == "unemploy":
            return render_template("/unempl.html")
        if graph == "poverty":
            return render_template("/pov.html")
        if graph == "education":
            return render_template("/edu.html")



@app.route("/observations")
def observations():
    return render_template("observations.html")

@app.route("/rawdata")
def data():
    return render_template("rawdata.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not request.form.get("first"):
            return apology("must provide first name", 403)
        if not request.form.get("last"):
            return apology("must provide last name", 403)
        if not request.form.get("email"):
            return apology("must provide email", 403)
        if not request.form.get("comment"):
            return apology("must provide comment", 403)

        first = request.form.get("first")
        last = request.form.get("last")
        email = request.form.get("email")
        comment = request.form.get("comment")

        db.execute("INSERT INTO contact (first, last, email, comment) VALUES(:first, :last, :email, :comment)",
            first=first, last=last, email=email, comment=comment)

        # Thank you message
        flash("Thanks for your feedback!")
        return redirect("/")

    else:
        return render_template("contact.html")