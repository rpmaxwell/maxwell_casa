from models import *
from app import app
from flask import Flask
from flask import request, render_template, flash, redirect, session, abort, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from config import BaseConfig
from flask_wtf.csrf import CSRFProtect

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        post = Post(text)
        db.session.add(post)
        db.session.commit()
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/quizbowl')
def quiz():
    return render_template("quizbowl.html")


@app.route("/hello")
def hello():
    return "Hello World!"



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # flash('ready to go for {} with password {}'.format(form.username.data, form.password.data))
        user = User(form.username.data, form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('hello'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    flash('test!')
    if current_user.is_authenticated:
        return redirect(url_for('secret'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('it was a post!')
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Failed with username {} and password {}'.format(user, form.password.data))
            flash('hashed password: {}'.format(user.check_password(form.password.data)))
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('secret'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/secret')
@login_required
def secret():
    return "Secret as hell"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))