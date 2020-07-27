# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
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
@app.route('/library')
def indexlibrary():
    return render_template('library_index.html')

@app.route('/')
@app.route('/collections')
def indexcollection():
    return render_template('collections.html')

@app.route('/')
@app.route('/playlists')
def indexplaylist():
    return render_template('playlists.html')

# CONNECT TO DB, ADD DATA

@app.route('/add')
def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""
