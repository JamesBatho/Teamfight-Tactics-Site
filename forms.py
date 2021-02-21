from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(),Email()])

    summoner_name = StringField('Summoner Name')
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')

class UserEditForm(FlaskForm):
    """Form for editing users"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6),DataRequired()])