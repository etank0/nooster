from flask import request, session, redirect, render_template
from functools import wraps
import os, requests


API_KEY = os.environ.get("API_KEY")

# Dictionaries
countries = [
    {"UAE" : "ae"},
    {"Argentina" : "ar"},
    {"Austria" : "at"},
    {"Australia" : "au"},
    {"Belgium" : "be"},
    {"Bulgaria" : "bg"},
    {"Brazil" : "br"},
    {"Canada" : "ca"},
    {"Switzerland" : "ch"},
    {"China" : "cn"},
    {"Colombia" : "co"},
    {"Cuba" : "cu"},
    {"Czechia" : "cz"},
    {"Germany" : "de"},
    {"Egypt" : "eg"},
    {"France" : "fr"},
    {"Great Britain & Northern Ireland" : "gb"},
    {"Greece" : "gr"},
    {"Hong Kong" : "hk"},
    {"Hungary" : "hu"},
    {"Indonesia" : "id"},
    {"Ireland" : "ie"},
    {"Israel" : "il"},
    {"India" : "in"},
    {"Italy" : "it"},
    {"Japan" : "jp"},
    {"South Korea" : "kr"},
    {"Lithuania" : "lt"},
    {"Latvia" : "lv"},
    {"Morocco" : "ma"},
    {"Mexico" : "mx"},
    {"Malaysia" : "my"},
    {"Nigeria" : "ng"},
    {"Netherlands" : "nl"},
    {"Norway" : "no"},
    {"New Zealand" : "nz"},
    {"Phillipines" : "ph"},
    {"Poland" : "pl"},
    {"Portugal" : "pt"},
    {"Romania" : "ro"},
    {"Serbia" : "rs"},
    {"Russia" : "ru"},
    {"Saudi Arabia" : "sa"},
    {"Sweden" : "se"},
    {"Singapore" : "sg"},
    {"Slovenia" : "si"},
    {"Slovakia" : "sk"},
    {"Thailand" : "th"},
    {"Turkey" : "tr"},
    {"Taiwan" : "tw"},
    {"Ukraine" : "ua"},
    {"United States Of America" : "us"},
    {"Venezuela" : "ve"},
    {"South Africa" : "za"}
]

country_list = []
for country in countries:
    co = list(country.keys())[0]
    country_list.append(co)

categories = [
    "business",
    "entertainment", 
    "general", 
    "health", 
    "science", 
    "sports", 
    "technology"
]

# login_required decorator
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# error function for any errors
def error(message):
    return render_template("error.html", message=message)

# to get topheadline articles
def getHeadlines(country="us", category="technology"):
    url = "https://newsapi.org/v2/top-headlines?country={}&category={}&apiKey={}"
    try:
        response = requests.get(url.format(country, category, API_KEY)).json()
    except:
        return 400

    if response["status"] != "ok" or not response['totalResults']:
        return 401

    articles = response["articles"][0:20]
    
    return articles

