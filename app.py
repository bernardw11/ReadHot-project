# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

from googlebookstests import search
from openlibrary import findsubjects
import spotifytests

from flask_pymongo import PyMongo


# -- Initialization section --
app = Flask(__name__)


# name of database
app.config['MONGO_DBNAME'] = 'ReadHot'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:prs2SF3EVpFvOAbR@cluster0.vgebo.mongodb.net/ReadHot>?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/library', methods=['GET', 'POST'])

def library():
    return render_template('library_index.html', time = datetime.now())

@app.route('/collections')

def collections():
    return render_template('collections.html', time = datetime.now())

@app.route('/playlists', methods = ["GET", "POST"])
def playlists():
    if request.method == "POST":
        feature = request.form['feature']
        playlistid = spotifytests.create_playlist(f"New playlist: {feature}", feature, ">", 0.7)
        return render_template('playlists.html', time = datetime.now(), playlistid = playlistid)
    else:
        return render_template('playlists.html', time = datetime.now())

@app.route('/template')
def template():
    return render_template('template.html', time = datetime.now())

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


@app.route('/login-page')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form.get('username', False)})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template('signup.html')