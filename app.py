from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify

from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Champion, Item, Piece, Composition
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, UserEditForm, LoginForm
import os 

API_KEY = "RGAPI-b6ccae62-33b9-4a6e-bbcd-c639323bb92a";

CURR_USER_KEY = 'curr_user_id'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgres:///tft-site')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']= True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"

debug = DebugToolbarExtension(app)


########################
#user signup/login/logout

@app.before_request
def add_user_to_go():
    """If logged in, add current user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user. """
    session[CURR_USER_KEY] = user.id 

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup',methods=["GET","POST"])
def signup():
    """Handle user signup

    Create new user and add to DB, redirect to homepage

    If form not valid re-present form with error messages

    if user already exists with that username: flash message and re-present form"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data,first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, summoner_name=form.summoner_name.data)
            
            db.session.commit()
        except IntegrityError:
            flash("Username already taken","danger")
            return render_template('users/signup.html',form=form)
        
        do_login(user)
        return redirect('/')
    else:
        return render_template('users/signup.html',form=form)

@app.route('/login',methods=["GET","POST"])
def login():
    """Handle users login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,form.password.data)

        if user:
            do_login(user)
            flash(f"Hello {user.username}!", "success")
            return redirect('/')
        
        flash("Invalid credentials", "danger")
    return render_template("users/login.html",form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("Successfully logged out","success")
    return redirect('/')
        
#composition builder
@app.route('/teambuilder')
def teambuilder():
    """Provide functional teambuilder for user"""
    champions = []
    idx = 0
    for filename in os.listdir('static/data/champions'):
        idx = idx + 1 
        champions.append((os.path.join('static/data/champions',filename),idx))
    return render_template('teambuilder.html',champions=champions)
##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: homepage with 10 most recent compostions and login button 
    - logged in: recent comps on right, own comps on left, buttons for teambuilder and champ explorer 
    """

    ####get 10 most recent compositons 
    # recents = (Composition.query.order_by(Composition.timestamp.desc().limit(10).all()))
    recents = 'hi'
    if g.user:
       #get user compositions
    #    own_comps = (Composition.query.filter(Composition.creator_id == g.user.id).all())
       own_comps = "hey"
       summoner_name = g.user.summoner_name
       summoner_info = requests.get(f'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?api_key={API_KEY}')
       puuid = summoner_info.json()['puuid']

       match_list = requests.get(f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=20&api_key={API_KEY}')

       matches = match_list.json()
       match_data = []

       for match in matches:
           match_info = requests.get(f'https://americas.api.riotgames.com/tft/match/v1/matches/{match}?api_key={API_KEY}')
           match_json = match_info.json()['info']
           game_length = round(match_json['game_length']/60,2)
           for participant in match_json['participants']:
               if participant['puuid'] == puuid:
                   placement = participant['placement']
                   game_data = {'game_length':game_length, 'placement':placement}
                   match_data.append(game_data)

       return render_template('home.html', recents = recents, own_comps = own_comps, match_data = match_data)

    else:
        return render_template('home-anon.html',recents = recents)

###########
@app.route('/save', methods=["POST"])
def save_comp():

    return 'hi'


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
