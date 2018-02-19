import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os
from project import db
from project.models import FlockRoster

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def connect_to_gsheets():
    scope = ['https://spreadsheets.google.com/feeds']
    cred_file = os.path.join(APP_ROOT, '.gsheets_creds.json')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
    return credentials


def get_sheep_data():
    credentials = connect_to_gsheets()
    url = os.environ['SHEEP_SHEET']
    gc = gspread.authorize(credentials)
    sh = gc.open_by_url(url)
    worksheet = sh.worksheet("roster")
    sheep_data = worksheet.get_all_records()
    return sheep_data


def commit_worksheet_data():
    FlockRoster.query.delete()
    sheep_data = get_sheep_data()
    for row in sheep_data:
        for k, v in row.items():
            if k in ['date_acquired', 'disposition_date']:
                try:
                    datetime.strptime(v, '%m/%d/%Y')
                except:
                    row[k] = None  
            elif k == 'tag_number':
                row[k] = str(v)
            elif v == '':
                row[k] = None
            elif k in ['is_ewe', 'is_current']:
                if v == 'TRUE':
                    row[k] = True
                elif v == 'FALSE':
                    row[k] = False
                else:
                    row[k] = None
        sheep_record = FlockRoster(**row)
        db.session.add(sheep_record)
        db.session.commit()