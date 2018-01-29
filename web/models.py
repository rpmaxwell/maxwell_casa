# models.py

from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from app import db



class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)

    def __init__(self, text):
        self.text = text
        self.date_posted = datetime.datetime.now()


class User(UserMixin, db.Model):
    """"""
    __tablename__ = "registered_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    registration_start = db.Column(db.DateTime, nullable=True)
 
    def __init__(self, username, email):
        """"""
        self.username = username
        self.email = email
        self.date_posted = datetime.datetime.now()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)], render_kw={"placeholder": "username"})
    email = StringField('Email Address', [validators.Length(min=6, max=35)], render_kw={"placeholder": "email"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "confirm password"})


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


class FlockRoster(db.Model):
    __tablename__ = 'flock_roster'

    id = db.Column(db.Integer, primary_key=True)
    tag_number = db.Column(db.String)
    given_name = db.Column(db.String)
    acquisition_source = db.Column(db.String)
    date_acquired = db.Column(db.DateTime)
    is_ewe = db.Column(db.Boolean)
    is_current = db.Column(db.Boolean)
    disposition_date = db.Column(db.DateTime)
    fate = db.Column(db.String)
    picture = db.Column(db.String)