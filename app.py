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
app.config['MONGO_URI'] = 'mongodb+srv://admin:prs2SF3EVpFvOAbR@cluster0.vgebo.mongodb.net/ReadHot?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/library', methods=['GET', 'POST'])
def library():
    #if ur logged in, use books = user_books and username = session['username'].
    if session.get('username'):
        collection = mongo.db.books
        user_books = collection.find({'user': session['username']})

        if request.method == "POST":
            playlistid = request.form['playlistid']
            return render_template('newlibrary.html', time = datetime.now(), playlistid = playlistid, username = session.get('username'), books = user_books, display = session.get('display'))
        else:
            return render_template('newlibrary.html', time = datetime.now(), username = session.get('username'), books = user_books, display = session.get('display'))
    #if ur not logged in, just show the demo page.
    else:
        if request.method == "POST":
            playlistid = request.form['playlistid']
            return render_template('library_index.html', time = datetime.now(), playlistid = playlistid)
        else:
            return render_template('library_index.html', time = datetime.now())

@app.route('/library_search', methods = ["GET", "POST"])
def searchbooks():
    if session.get('username'):
        if request.method == "POST":
            searchquery = request.form['bookchoice']
            books = search(searchquery)
            return render_template("library_search.html", time = datetime.now(), books = books, username = session.get('username'), display = session.get('display'))
        else:
            return render_template("library_search.html", time = datetime.now(), username = session.get('username'), display = session.get('display'))
    else:
        redirect(url_for('login_page'))

# ''' The following may be added later:
# @app.route('/collections')
# def collections():
#     return render_template('collections.html', time = datetime.now())
#
# @app.route('/playlists', methods = ["GET", "POST"])
# def playlists():
#     if request.method == "POST":
#         feature = request.form['feature']
#         playlistid = spotifytests.create_playlist(f"New playlist: {feature}", feature, ">", 0.7)
#         return render_template('playlists.html', time = datetime.now(), playlistid = playlistid)
#     else:
#         return render_template('playlists.html', time = datetime.now())
#
# @app.route('/template')
# def template():
#     return render_template('template.html', time = datetime.now())
# '''

# CONNECT TO DB, ADD DATA
@app.route('/add_book', methods = ['GET', 'POST'])
def add_book():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        isbn = request.form['isbn']
        coverurl = request.form['coverurl']
        subjects = findsubjects(title, author)

        user = session['username']
        display = session['display']

        playlistid = spotifytests.generate_playlist(title, author, description, subjects, display)
        collection = mongo.db.books
        collection.insert({
            'title': title,
            'author': author,
            'description': description,
            'subjects': subjects,
            'isbn': isbn,
            'coverurl': coverurl,
            'user': user,
            'playlistid': playlistid
        })

        return redirect(url_for('library'))


@app.route('/login_page')
def login_page():
    return render_template('login_page.html', time=datetime.now())


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username': request.form['username']})
    #login_user = users.find_one({'username': request.form.get('username', False)})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            session['display'] = login_user['display']
            return redirect(url_for('library'))
        return redirect(url_for('login_page'))
    return render_template('signup.html', time=datetime.now())

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            users.insert({'display': request.form['display'], 'username' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            session['display'] = request.form['display']
            return redirect(url_for('library'))
        return 'That username already exists! Try logging in.'
    return render_template('signup.html', time=datetime.now())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))
