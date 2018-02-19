from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from project import db


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
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, default='user')

 
    def __init__(self, first_name, last_name, email, role='user'):
        """"""
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.registered_on = datetime.datetime.now()
        self.role = role
        self.authenticated = False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated


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