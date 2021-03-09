"""SQLAlchemy models for TFT site"""

from datetime import datetime
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User of the site"""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
    )


    summoner_name = db.Column(db.Text)

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(db.Text)

    last_name = db.Column(db.Text)

    password = db.Column(db.Text,nullable=False)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email} {self.summoner_name}"

    @classmethod 
    def signup(cls,username,email,password,first_name,last_name,summoner_name):
        """Sign up user. Hashes password and adds user to the system"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username,email=email,first_name=first_name,last_name= last_name, password= hashed_pwd, summoner_name=summoner_name)

        db.session.add(user)
        return user

    @classmethod 
    def authenticate(cls, username,password):
        """Find user with username and password if exists otherwise return false"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password,password) 
            if is_auth:
                return user
        
        return False

class Champion(db.Model):
    """Champion Data"""
    __tablename__ = 'champions'
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    champ_name = db.Column(db.Text,nullable=False)

    img = db.Column(db.Text)

class Item(db.Model):
    """Item Data""" 
    __tablename__ = 'items'
    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    description = db.Column(db.Text)

    stat_modifier = db.Column(db.Text)

    stat_amount = db.Column(db.Integer, default=15)

class Piece(db.Model):
    """Board Piece Data"""

    __tablename__ = 'pieces'
    
    id = db.Column(db.Integer,primary_key=True,)

    champion_id = db.Column(db.Integer, db.ForeignKey('champions.id'))

    position = db.Column(db.Integer, nullable = False)

    item1_id = db.Column(db.Integer,db.ForeignKey('items.id'))

    item2_id = db.Column(db.Integer,db.ForeignKey('items.id'))

    item3_id = db.Column(db.Integer,db.ForeignKey('items.id'))

class Composition(db.Model):
    """Composition Data"""

    __tablename__ = 'compositions'
    
    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.Text, nullable= False)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    piece1_id = db.Column(db.Integer, db.ForeignKey('pieces.id', ondelete="cascade"))
    piece2_id = db.Column(db.Integer, db.ForeignKey('pieces.id', ondelete="cascade"))
    piece3_id = db.Column(db.Integer, db.ForeignKey('pieces.id', ondelete="cascade"))
    piece4_id = db.Column(db.Integer, db.ForeignKey('pieces.id', ondelete="cascade"))
    piece5_id = db.Column(db.Integer, db.ForeignKey('pieces.id', ondelete="cascade"))
    piece6_id = db.Column(db.Integer, db.ForeignKey('pieces.id', ondelete="cascade"))
    piece7_id = db.Column(db.Integer, db.ForeignKey('pieces.id', ondelete="cascade"))
    piece8_id = db.Column(db.Integer, db.ForeignKey('pieces.id', ondelete="cascade"))



    damage_score = db.Column(db.Float)
    utility_score = db.Column(db.Float)
    total_score = db.Column(db.Float)

def connect_db(app):
    """Connect this database to provided Flask app.
    call this in Flask app"""

    db.app = app
    db.init_app(app)
