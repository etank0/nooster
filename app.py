import os
from flask import Flask, render_template, redirect, session, flash, jsonify, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import requests

from modules import login_required, error, categories, countries, country_list, getHeadlines

# instantiate the db
db = SQLAlchemy()

# starting the web app
app = Flask(__name__)

# checking for API_KEY
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set!")

# config for the databse
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nooster.db"

db.init_app(app)

# creating a class to represent the table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    pref = db.Column(db.Integer)

class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, unique=True, nullable=False)
    countryid = db.Column(db.Integer)
    category = db.Column(db.String, nullable=False)

class Bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    imageurl = db.Column(db.String)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    user_id = session["user_id"]
    pref = int(User.query.filter_by(id=user_id).first().pref)


    if not pref:
        articles = getHeadlines()
    else:
        pref_entry = Preferences.query.filter_by(userid=user_id).first()
        # finding countrycode
        counid = pref_entry.countryid
        councode = countries[counid][country_list[counid]]

        articles = getHeadlines(councode, pref_entry.category)

    

    if articles == 400:
        return error("API Side Connection Error!")
    elif articles == 401:
        return error("API Side Problem and/or No results found!")

    index = None

    if request.method == "POST":
        index = int(request.form.get("article-index"))
        pref_article = articles[index]

        if not pref_article:
            return error("HTML tweaking or/and some index error occurred!")

        bkentries = Bookmarks.query.filter_by(userid=user_id).all()

        if len(bkentries) > 10:
            return error("Article not bookmarked! Maximum no. of articles(10) reached!")

        # Adding entry to the table
        book_entry = Bookmarks(
            userid=user_id,
            title=pref_article["title"],
            url=pref_article["url"],
            imageurl=pref_article["urlToImage"])

        db.session.add(book_entry)
        db.session.commit()
        flash("News article bookmarked!")
        return redirect("/")

    return render_template("index.html", pref=pref, articles=articles)


@app.route("/bookmarks", methods=["GET", "POST"])
@login_required
def bookmarks():
    user_id = session["user_id"]

    # Getting all the bookmarks of the user
    bktable = Bookmarks.query.filter_by(userid=user_id).all()

    exist = 1
    if not bktable:
        exist = 0

    if len(bktable) >= 10:
        flash("Bookmarks full! Remove some to add other articles!")

    if request.method == "POST":
        index = int(request.form.get("book-index"))

        xentry = bktable[index]
        if not xentry:
            return error("HTML tweaking or/and some index error occurred!")

        db.session.delete(xentry)
        db.session.commit()
        flash("Bookmark removed!")
        return redirect("/bookmarks")

    return render_template("bookmarks.html", exist=exist, bktable=bktable)

@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    user_id = session["user_id"]
    entry = Preferences.query.filter_by(userid=user_id).first()

    pref = 0
    en_countryid = -1
    en_category = ""

    if entry:
        pref = 1
        en_countryid = entry.countryid
        en_category = entry.category

    if request.method == "POST":
        pref_country = request.form.get("country")
        pref_category = request.form.get("category")
        pref_conid = country_list.index(pref_country)

        if entry:
            entry.countryid = pref_conid
            entry.category = pref_category
        else:
            
            
            obj = Preferences(userid=user_id, countryid=pref_conid, category=pref_category)
            user_obj = User.query.filter_by(id=user_id).first()
            user_obj.pref = 1
            db.session.add(obj)
        db.session.commit()

        flash("Preferences Updated!")
        return redirect("/")

    return render_template(
        "preferences.html", 
        countries=country_list,
        categories=categories, 
        en_country=en_countryid,
        en_category=en_category,
        pref=pref
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registering User"""
    if request.method == "POST":
        # Getting results from the Form
        user = request.form.get("username")
        passw = request.form.get("password")
        repassw = request.form.get("repassword")

        # Validating the form results
        if not user:
            return error("Provide Username!")
        if not passw or not repassw:
            return error("Provide Password In Both Fields!")
        if passw != repassw:
            return error("Passwords Mismatch!")
        if not user.isalnum() or len(user) < 6:
            return error("Username contains special character and/or less than 6 characters!") 
        if not passw.isalnum() or len(passw) < 4:
            return error("Password contains special character and/or less than 4 characters!")

        if User.query.filter_by(username=user).first():
            return error("Username already exists!")
        # Creating user and updating the database
        entry = User(username=user, hash=generate_password_hash(passw), pref=0)

        db.session.add(entry)
        db.session.commit()

        flash("Successfully Registered! Please Login!")

        return redirect("/login")

    flash("Warning! Don't use your actual password from some other website!")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Logging User IN"""
    if request.method == "POST":
        # Getting results from the form
        user = request.form.get("username")
        passw = request.form.get("password")

        if not user or not passw:
            return error("Username and/or Password field was empty!")

        entry = User.query.filter_by(username=user).first()

        if not entry or not check_password_hash(entry.hash, passw):
            return error("Invalid Username and/or Password!")

        # Remember which user has logged in
        session["user_id"] = entry.id

        flash(f"Welcome! {user}.")
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/chat")
def chat():
    """ChatBox Route"""
    return render_template("chat.html")

if __name__ == "__main__":
    # creating the tables
    with app.app_context():
        db.create_all()
   
    app.run(host='127.0.0.1',port=8000,debug=True)