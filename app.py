from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify

from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Champion, Item, Piece, Composition
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, UserEditForm, LoginForm
import os 

import pdb 

from secrets import API_KEY

CURR_USER_KEY = 'curr_user_id'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgres:///tft-site')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO']= True
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
        
#composition builder for users to build their compositions


@app.route('/teambuilder')
def teambuilder():
    """Provide functional teambuilder for user"""
    if g.user: 
        champions = db.session.query(Champion).all()
        return render_template('teambuilder.html',champions=champions)
    else: 
        return redirect('/')

@app.route('/teambuilder/<int:comp_id>')
def edit_comp(comp_id):
    if g.user: 
        """allow user to edit comp and then save"""
        comp = Composition.query.get_or_404(comp_id)
        peice_ids = (comp.piece1_id,comp.piece2_id,comp.piece3_id,comp.piece4_id,comp.piece5_id,comp.piece6_id,comp.piece7_id,comp.piece8_id)
        pieces = db.session.query(Piece).filter(Piece.id.in_(peice_ids)).all()
        champ_ids = []
        pos = [] 
        for piece in pieces:
            champ_ids.append(piece.id)
            pos.append(piece.position)
        champs = db.session.query(Champion).filter(Champion.id.in_(tuple(champ_ids))).all()

        board = []
        i = 0
        while i < len(champs):
            board.append([champs[i].img, champs[i].id, pos[i]])
            i = i +1
        
        champions = db.session.query(Champion).all()
        return render_template('edit_comp.html', comp = comp, champions=champions, pieces = pieces, champs = champs, board = board)
    else:
        return redirect('/')


##############################################################################
#Route for allowing the user to view other compositions- this will not be editable
@app.route('/teamviewer/<int:comp_id>')
def view_comp(comp_id):
       # allow anyone to view compositions
        comp = Composition.query.get_or_404(comp_id)
        peice_ids = (comp.piece1_id,comp.piece2_id,comp.piece3_id,comp.piece4_id,comp.piece5_id,comp.piece6_id,comp.piece7_id,comp.piece8_id)
        pieces = db.session.query(Piece).filter(Piece.id.in_(peice_ids)).all()
        champ_ids = []
        pos = [] 
        for piece in pieces:
            champ_ids.append(piece.id)
            pos.append(piece.position)
        champs = db.session.query(Champion).filter(Champion.id.in_(tuple(champ_ids))).all()

        board = []
        i = 0
        while i < len(champs):
            board.append([champs[i].img, champs[i].id, pos[i]])
            i = i +1
        
        champions = db.session.query(Champion).all()
        return render_template('view_comp.html', comp = comp, champions=champions, pieces = pieces, champs = champs, board = board)
   




# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: homepage with 10 most recent compostions and login button 
    - logged in: recent comps on right, own comps on left, buttons for teambuilder and champ explorer 
    """
    recents = db.session.query(Composition).order_by(Composition.timestamp.desc()).limit(10).all()
    ####get 10 most recent compositons 
    if g.user:

       #get user compositions
       own_comps = db.session.query(Composition).filter(Composition.creator_id == g.user.id).all()
       try: 
           summoner_name = g.user.summoner_name
           print(summoner_name)
           summoner_info = requests.get(f'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?api_key={API_KEY}')
           puuid = summoner_info.json()['puuid']
           print(puuid)
           match_list = requests.get(f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=20&api_key={API_KEY}')
           matches = match_list.json()
           if len(matches) == 0: 
                raise(IntegrityError)
           match_data = []
           
           for match in matches:
               match_info = requests.get(f'https://americas.api.riotgames.com/tft/match/v1/matches/{match}?api_key={API_KEY}')
               match_json = match_info.json()['info']
               game_length = round(match_json['game_length']/60,2)
               print(game_length)
               for participant in match_json['participants']:
                   if participant['puuid'] == puuid:
                       placement = participant['placement']
                       print(placement)
                       game_data = {'game_length':game_length, 'placement':placement}
                       match_data.append(game_data)
                       print(match_data)
                
           return render_template('home.html', recents = recents, own_comps = own_comps, match_data = match_data)
       except:
           return render_template('home.html',recents = recents, failed=True, own_comps = own_comps)
    else:
        return render_template('home-anon.html',recents = recents)

###########
@app.route('/save', methods=["POST"])
def save_comp():
    if g.user:

        datas = request.json
        data = datas[0]
        name = datas[1]
        print(len(data))
        print(data[0][0],data[0][1])
        i = 0 
        pieces = []
        while i < len(data):
            piece = Piece(champion_id=data[i][1],position=data[i][0])
            pieces.append(piece)
            db.session.add(piece)
            db.session.commit()
            i = i+1
        
        comp = Composition(name=name, creator_id=g.user.id, piece1_id=pieces[0].id, piece2_id=pieces[2].id, piece3_id=pieces[2].id,piece4_id=pieces[3].id,piece5_id=pieces[4].id,piece6_id=pieces[5].id,piece7_id=pieces[6].id,piece8_id=pieces[7].id)

        db.session.add(comp)
        db.session.commit()
        return 'added comp'


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
