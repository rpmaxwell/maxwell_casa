# app.py
from flask import Flask
from flask import request, render_template, flash, redirect, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from config import BaseConfig
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from threading import Lock


from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

async_mode = 'threading'
socketio = SocketIO(app, async_mode=async_mode)
sensor_thread = None
device_thread = None
thread_lock = Lock()

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


@app.route('/garden')
def home_garden():
    sensor_data = get_latest_sensor_readings()
    device_data = get_device_status()
    return render_template('garden_dashboard.html', sensor_data=sensor_data, device_data=device_data, async_mode=socketio.async_mode)

@csrf.exempt
def device_background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(3)
        device_data = get_device_status()
        if device_data:
            socketio.emit('device_status', device_data, namespace='/device_reading')
        else:
            print('missing device readings!')

@csrf.exempt
def sensor_background_thread():
    while True:
        socketio.sleep(15)
        sensor_data = get_latest_sensor_readings()
        if sensor_data:
            socketio.emit('sensor_reading', sensor_data, namespace='/device_reading')
        else:
            print('missing sensor readings!')


@socketio.on('connected', namespace='/device_reading')
@csrf.exempt
def quizbowl_connected():
    socketio.emit('connection_confirmed', {'message': 'connected'}, namespace='/device_reading')


@socketio.on('buzz_request', namespace='/device_reading')
def relay_buzz_request(msg):
    print('we have a buzz')
    socketio.emit('buzz', msg, namespace='/device_reading')


@socketio.on('connect', namespace='/device_reading')
@csrf.exempt
def get_connected():
    global sensor_thread
    global device_thread
    with thread_lock:
        if sensor_thread is None:
            sensor_thread = socketio.start_background_task(target=sensor_background_thread)
        if device_thread is None:
            device_thread = socketio.start_background_task(target=device_background_thread)
    emit('my_response', {'message': 'Connected'}, namespace='/device_reading')


from project.users.views import users_blueprint
from project.garden.views import garden_blueprint, get_device_status, get_latest_sensor_readings
from project.sheep.views import sheep_blueprint
from project.home_library.views import home_library_blueprint
app.register_blueprint(users_blueprint)
app.register_blueprint(garden_blueprint)
app.register_blueprint(sheep_blueprint)
app.register_blueprint(home_library_blueprint)

csrf.exempt(garden_blueprint)


