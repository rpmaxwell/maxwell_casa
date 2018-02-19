from flask import Blueprint, render_template
from project.models import FlockRoster

sheep_blueprint = Blueprint('sheep', __name__)


@sheep_blueprint.route('/sheep_roster')
def sheep_roster():
    rows = FlockRoster.query.filter(FlockRoster.is_current.is_(True)).all()
    return render_template('sheep.html', rows=rows)


@sheep_blueprint.route('/sheep_cam')
def sheep_cam():
	return render_template('sheep_cam.html')
