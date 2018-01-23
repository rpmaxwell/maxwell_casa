# app.py
from flask import Flask
from flask import request, render_template, flash, redirect, session, abort, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from config import BaseConfig
from flask_wtf.csrf import CSRFProtect, generate_csrf
import requests

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect(app)
csrf.init_app(app)

from models import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @app.route('/', methods=['GET', 'POST'])
# def menu():
#     if request.method == 'POST':
#         text = request.form['text']
#         post = Post(text)
#         db.session.add(post)
#         db.session.commit()
#     posts = Post.query.order_by(Post.date_posted.desc()).all()
#     return render_template('index.html', posts=posts)


@app.route('/', methods=['GET'])
def menu():
    return render_template('menu.html')


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
        login_user(user, remember=True)
        return redirect(url_for('menu'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/secret')
@login_required
def secret():
    return "Secret as hell"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('menu'))

@app.route('/sheep')
def sheep():
    return render_template('sheep.html')


@app.route('/lights', methods=['GET', 'POST'])
def lights():
    # if not current_user.is_authenticated:
    #     return redirect(url_for('login'))
    if request.method == 'GET':
        lamp_status = requests.get('http://192.168.1.195:5000/lamp_status').text
    elif request.method == 'POST':
        requests.get('http://192.168.1.195:5000/api')
        lamp_status = requests.get('http://192.168.1.195:5000/lamp_status').text
    return render_template('lights.html', payload={'status': lamp_status})
        
        


# @app.route('/light_status/', methods=['GET', 'POST'])
# def get_light_status():



if __name__ == '__main__':
    app.run()
