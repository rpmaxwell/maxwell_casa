# create_db.py

from project import db, app
from project.sheep import gsheets_model
from project.home_library import home_library_model
from project.models import FlockRoster, User


with app.app_context():
    db.create_all()


# user = User('Rob', 'Euclid', 'rpmaxwell144@gmail.com')
# user.set_password('test1')
# db.session.add(user)
# db.session.commit()

gsheets_model.commit_worksheet_data()
home_library_model.commit_worksheet_data()
