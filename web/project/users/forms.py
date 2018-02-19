from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message='first name required!'),
        Length(max=40, message='too long!'),
    ], render_kw={"placeholder": "first name"})
    last_name = StringField('Last Name', validators=[
        DataRequired(message='last name required!'),
        Length(max=40, message='too long!'),
    ], render_kw={"placeholder": "first name"})
    email = StringField('Email Address', validators=[
    	DataRequired(message='email required!'),
    	Email(message='must be a valid email address'),
    	Length(min=6, max=40, message='either too short or too long.'),
    ], render_kw={"placeholder": "email"})
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, max=40, message='must be between 6 and 40 characters'),
        EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "confirm password"})


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(),
        Email(),
        Length(min=6, max=40)
    ], render_kw={"placeholder": "email"})
    password = PasswordField('Password', [DataRequired()
    ], render_kw={'placeholder': 'password'})