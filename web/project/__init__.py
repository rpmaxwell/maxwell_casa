# app.py
from flask import Flask
from flask import request, render_template, flash, redirect, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from config import BaseConfig
from flask_wtf.csrf import CSRFProtect, generate_csrf


from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)


csrf = CSRFProtect(app)
csrf.init_app(app)

from project import models


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('menu'))


@app.route('/', methods=['GET'])
def menu():
    return render_template('menu.html')


@app.route('/quizbowl')
def quiz():
    return render_template("quizbowl.html")


@app.route("/hello")
def hello():
    return "Hello World!"

from project.users.views import users_blueprint
from project.home_automation.views import home_automation_blueprint
from project.sheep.views import sheep_blueprint
app.register_blueprint(users_blueprint)
app.register_blueprint(home_automation_blueprint)
app.register_blueprint(sheep_blueprint)

 


