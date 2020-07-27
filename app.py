# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request
from datetime import datetime
from openlibrary import search
# from flask_pymongo import PyMongo


# # -- Initialization section --
app = Flask(__name__)

# events = [
#         {"event":"First Day of Classes", "date":"2019-08-21"},
#         {"event":"Winter Break", "date":"2019-12-20"},
#         {"event":"Finals Begin", "date":"2019-12-01"}
#     ]

# name of database
# app.config['MONGO_DBNAME'] = 'database-name'

# URI of database
# app.config['MONGO_URI'] = 'mongo-uri'

# mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/indexlibrary')

def indexlibrary():
    return render_template('library_index.html')

@app.route('/')
@app.route('/indexcollection')

def indexcollection():
    return render_template('collections.html')

@app.route('/')
@app.route('/indexplaylist')

def indexplaylist():
    return render_template('playlists.html')




@app.route('/library_search', methods = ["GET", "POST"])
def searchbooks():
    if request.method == "POST":
        searchquery = request.form['bookchoice']
        books = search(searchquery)
        return render_template("library_search.html", time = datetime.now(), books = books)
    else:
        return render_template("library_search.html", time = datetime.now())

# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""
