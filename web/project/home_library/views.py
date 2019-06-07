from flask import Blueprint, render_template
from project.models import HomeLibrary

home_library_blueprint = Blueprint('home_library', __name__)


@home_library_blueprint.route('/library')
def home_library():
    rows = HomeLibrary.query.all()
    return render_template('home_library.html', rows=rows)
