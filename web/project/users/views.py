
from flask import Flask
from flask import Blueprint, request, render_template, flash, redirect, session, url_for
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from project import db
from project.models import User
from .forms import RegistrationForm, LoginForm
from datetime import datetime

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        try:
            user = User(form.first_name.data, form.last_name.data, form.email.data)
            user.set_password(form.password.data)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
        except IntegrityError:
            flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
            db.session.rollback()
            return render_template('register.html', form=form)
        flash('You\'ve Registered! Thank you!')
        return redirect(url_for('menu'))
    else:
        return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Error! This user does not exist!', 'error')
        elif not user.check_password(form.password.data):
            flash('Error! Incorrect password for this user', 'error')
        else:
            user.authenticated = True
            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('menu'))
    return render_template('login.html', title='Sign In', form=form)


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('menu'))