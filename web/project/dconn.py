from datetime import datetime
import json
import os
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, insert, create_engine

class Conn(object):
    def __init__(self, environment=None, schema_name=None):
        """Create a shell to hold metadata."""
        self.schema_name = schema_name
        cred_payload = {'user': os.environ['GARDEN_USER'],'password': os.environ['GARDEN_PASS'],'host': os.environ['GARDEN_HOST'],'db': os.environ['GARDEN_NAME']}
        url = 'postgresql://{user}:{password}@{host}/{db}'.format(**cred_payload)
        self.engine = create_engine(url)
        self.metadata = MetaData(schema=schema_name)
        self.metadata.bind = self.engine

    def execute_raw_query(self, query, params=None):
        """Take a SQL query in string format and then executes in Presto."""
        params = params or {}
        proxy = self.engine.execute(sqlalchemy.text(query), params)
        try:
            results_obj = list(map(dict, proxy))
            return results_obj
        except:
            return None
