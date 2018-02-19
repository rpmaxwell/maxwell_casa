from flask import Flask
from flask import Blueprint, request, render_template, flash, redirect, session, url_for
from flask_login import current_user, login_required
import requests
import os

home_automation_blueprint = Blueprint('home_automation', __name__)
raspberry_pi_ip = os.environ['HOME_AUTOMATION_IP']
raspberry_pi_port = os.environ['HOME_AUTOMATION_PORT']

SERVICE_URL = '{}:{}'.format(raspberry_pi_ip, raspberry_pi_port)

@home_automation_blueprint.route('/lights', methods=['GET', 'POST'])
@login_required
def lights():
    if current_user.is_authenticated:   
        if request.method == 'GET':
            url = '{}:{}/lamp_status'.format(raspberry_pi_ip, raspberry_pi_port)
            try:
                r = requests.get(SERVICE_URL + '/lamp_status')
            except requests.exceptions.RequestException as e:
                return redirect(url_for('home_automation.no_lights'))
            if r.status_code != 200:
                return redirect(url_for('home_automation.no_lights'))
            lamp_status = r.text
        elif request.method == 'POST':
            requests.get(SERVICE_URL + '/api')
            lamp_status = requests.get(SERVICE_URL + '/lamp_status').text
        return render_template('lights.html', payload={'status': lamp_status})
    else:
        redirect(url_for('user.login'))


@home_automation_blueprint.route('/no_lights')
def no_lights():
    return render_template('no_lights.html')