import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os
from project import db
from project.models import HomeLibrary

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def connect_to_gsheets():
    scope = ['https://spreadsheets.google.com/feeds']
    cred_file = os.path.join(APP_ROOT, '.gsheets_creds.json')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
    return credentials


def get_book_data():
    credentials = connect_to_gsheets()
    url = os.environ['BOOK_SHEET']
    gc = gspread.authorize(credentials)
    sh = gc.open_by_url(url)
    worksheet = sh.worksheet("library_summary")
    book_data = worksheet.get_all_records()
    return book_data


def commit_worksheet_data():
    HomeLibrary.query.delete()
    book_data = get_book_data()
    for row in book_data:
        for k, v in row.items():
            if k == '':
                continue
            elif v == '':
                row[k] = None
            elif k == 'pages':
                row[k] = int(v)
        book_record = HomeLibrary(**row)
        db.session.add(book_record)
        db.session.commit()
