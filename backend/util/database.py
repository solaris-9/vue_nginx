from django.conf import settings
from dproject import settings as bs
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import logging
import pandas as pd

class DatabaseConnector:
    engine = None
    _db = None
    _cs = None
    def __init__(self, db):
        self._db = db
        key = db
        if db == 'bbddb':
          key = "default"
        self._cs = 'mysql+pymysql://{}:{}@{}:{}/'.format(
            bs.DATABASES[key]['USER'],
            quote_plus(bs.DATABASES[key]['PASSWORD']),
            bs.DATABASES[key]['HOST'],
            bs.DATABASES[key]['PORT']
          )
        self.engine = create_engine('{}{}'.format(self._cs, self._db), pool_pre_ping=True)
    def read_table(self, name):
        with self.engine.connect() as connection:
            df = pd.read_sql(name, connection)
        return df
        pass
    def read_query(self, query):
        with self.engine.connect() as connection:
            df = pd.read_sql_query(query, self.engine)
        return df
        pass
    def execute(self, cmd):
        try:
            with self.engine.begin() as conn:
                conn.execute(
                    text(cmd)
                )
                conn.commit()
        except Exception as e:
            logging.getLogger(__name__).debug('!!! ERROR: {}'.format(e))
        pass

    def close(self):
        self.session.close()
