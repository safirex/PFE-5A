from sqlalchemy import create_engine
from sqlalchemy.types import *
from enum import Enum

class DbTables(Enum):
    ''' set a fixed way to access db tables '''
    Test = 1


uri = 'mysql://root:eudeseude@localhost:3306/pfe'
engine = create_engine(uri, echo=False)
# conn = engine.connect('test_static_data')


def connect(db_table:DbTables):
    ''' return a sqlalchemy connexion to the db '''
    return engine,engine.connect(db_table.name)
