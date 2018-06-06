from flask import Flask, render_template, request, \
    redirect, jsonify, url_for, flash
from functools import wraps
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Movie, Genre, User
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(open('client_secrets.json', 'r'
                            ).read())['web']['client_id']


app = Flask(__name__)

# Connect to database
engine = create_engine('sqlite:///movieswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# login using google plus account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print (data)

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def login_required(f):
    @wraps(f)
    def decorated_function (*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed access")
            return redirect('/login')
    return decorated_function


# Log out of web site
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("successfully disconnected")
        return redirect(url_for('showGenres'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Genre JSON endpoint
@app.route('/genre/JSON', methods=['GET'])
def showGenresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres=[g.serialize for g in genres])


# JSON endpoint for movies in a genre
@app.route('/genre/<int:genre_id>/movies/JSON', methods=['GET'])
def showMoviesJSON(genre_id):
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    return jsonify(movies=[m.serialize for m in movies])


# JSON endpoint for a single movie
@app.route('/genre/<int:genre_id>/movies/<int:movie_id>/JSON', methods=['GET'])
def showOneMovieJSON(genre_id, movie_id):
    movie = session.query(Movie).filter_by(genre_id=genre_id,
                                           id=movie_id).one()
    return jsonify(movie.serialize)


# Displays all genres in database
@app.route('/')
@app.route('/genre/', methods=['GET'])
def showGenres():
    genres = session.query(Genre).all()
    if 'username' not in login_session:
        return render_template('publicgenres.html', genres=genres)
    else:
        return render_template('genres.html', genres=genres)


# Create a new genre
@app.route('/genre/new', methods=['GET', 'POST'])
@login_required
def newGenre():
    if request.method == 'POST':
        newgenre = Genre(name=request.form['name'],
                         description=request.form['description'],
                         user_id=login_session['user_id'])
        session.add(newgenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('newgenre.html')


# Edit a genre if the logged in user created the genre
@app.route('/genre/<int:genre_id>/edit', methods=['GET', 'POST'])
@login_required
def editGenre(genre_id):
    editedGenre = session.query(Genre).filter_by(id=genre_id).one()
    if editedGenre.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You are not
        authorized to edit this restaurant. Please create your own
        restaurant in order to
        edit.');}</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
        if request.form['description']:
            editedGenre.description = request.form['description']
        session.add(editedGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('editgenre.html', genre=editedGenre)


# Delete a genre if thee logged in user created the genre
@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteGenre(genre_id):
    genreToDelete = session.query(Genre).filter_by(id=genre_id).one()
    if genreToDeleteToDelete.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You are not 
        authorized to delete this restaurant. Please create your 
        own restaurant in order to 
        delete.');}</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        session.delete(genreToDelete)
        flash('%s Successfully Deleted' % genreToDelete.name)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('deletegenre.html', genre=genreToDelete)


# Shows all movies in a genre
@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/movies', methods=['GET'])
def showMovies(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    if 'username' not in login_session:
        return render_template('publicmovies.html', genre=genre, movies=movies)
    else:
        return render_template('movies.html', genre=genre, movies=movies)


# Create a new movie if the user is logged in
@app.route('/genre/<int:genre_id>/movies/new', methods=['GET', 'POST'])
@login_required
def newMovie(genre_id):
    if request.method == 'POST':
        newMovie = Movie(name=request.form['name'],
                         description=request.form['description'],
                         release_date=request.form['release_date'],
                         genre_id=genre_id,
                         user_id=login_session['user_id'])
        session.add(newMovie)
        session.commit()
        return redirect(url_for('showMovies', genre_id=genre_id))
    else:
        return render_template('newmovie.html', genre_id=genre_id)


# Edits a movie if the logged in user created the movie
@app.route('/genre/<int:genre_id>/movies/<int:movie_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editMovie(genre_id, movie_id):
    editedMovie = session.query(Movie).filter_by(id=movie_id).one()
    if login_session['user_id'] != editedMovie.user_id:
        return """<script>function myFunction() {alert('You
        are not authorized to edit menu items to this
        restaurant. Please create your own restaurant in
        order to edit
        items.');}</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['name']:
            editedMovie.name = request.form['name']
        if request.form['description']:
            editedMovie.description = request.form['description']
        if request.form['release_date']:
            editedMovie.release_date = request.form['release_date']
        session.add(editedMovie)
        session.commit()
        return redirect(url_for('showMovies', genre_id=genre_id))
    else:
        return render_template('editmovie.html', genre=editedMovie.genre_id,
                               movie=editedMovie)


# Delete a movie if the logged in user created the movie
@app.route('/genre/<int:genre_id>/movies/<int:movie_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteMovie(genre_id, movie_id):
    movieToDelete = session.query(Movie).filter_by(id=movie_id).one()
    if login_session['user_id'] != movieToDelete.user_id:
        return """<script>function myFunction() {alert('You are
        not authorized to delete menu items to this
        restaurant. Please create your own restaurant
        in order to delete
        items.');}</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        session.delete(movieToDelete)
        flash('%s Successfully Deleted' % movieToDelete.name)
        session.commit()
        return redirect(url_for('showMovies', genre_id=genre_id))
    else:
        return render_template('deletemovie.html',
                               genre_id=movieToDelete.genre_id,
                               movie=movieToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
