# create_db.py


from app import db
import gsheets_model

db.create_all()
gsheets_model.commit_worksheet_data()
