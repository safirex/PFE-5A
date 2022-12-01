from typing import Any
from importlib_metadata import metadata
from pandas import DataFrame
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.types import *
from enum import Enum
from files_format_enums import GTFSFilenames
from pathlib import Path
path = Path(__file__).parent / "./db.conf"


db_params = {}
def load_db_conf():
    f = open(path)
    for line in f:
        content = line.strip().replace(' ','').split('=')
        db_params[content[0]] = content[1]


class DbTables(Enum):
    ''' set a fixed way to access db tables '''
    Test = 1


load_db_conf()
db_sys  = db_params['db_sys']
db_host = db_params['db_host']
db_user = db_params['db_user']
db_pass = db_params['db_pass']
db_port = db_params['db_port']
uri = db_sys+'://'+db_user+':'+db_pass+'@'+db_host+':'+db_port+'/pfe2'

# uri = 'mysql://root:eudeseude@localhost:3306/pfe2'
# db_sys  = 'postgresql'
# db_host = 'localhost'
# db_user = 'dataprovider'
# db_pass = 'pleasework'
# db_port = '5432'
# uri = db_sys+'://'+db_user+':'+db_pass+'@'+db_host+':'+db_port+'/pfe'
engine = create_engine(uri, echo=False)

# engine.execute('SELECT current_user;')

# conn = engine.connect('test_static_data')


def connect(db_table:DbTables):
    ''' return a sqlalchemy connexion to the db '''
    return engine,engine.connect(db_table.name)
def get_engine():
    return engine
def getTable(tablename:str):
    return Table(tablename, MetaData(), autoload_with=get_engine())

def add_Data(dataframe,table_name,dtype=None,index=False,exists='fail'):
    print('exists = ',exists)
    dataframe.to_sql(
        table_name,
        engine,
        dtype = dtype,
        index=index,
        if_exists=exists
    )
    engine.execute
    print("success")

def insert_Data(dataframe:DataFrame,table_name,dtype=None):
    dataframe.to_sql(
        table_name,
        engine,
        dtype = dtype,
        index=False,
        if_exists='append',
    )
    engine.execute
    print("success")

def alter_table_add_pk(table:str,pkeys:str or list):
    if(type(pkeys)== list):
        pkeyline=""
        for pk in pkeys:
            if(len(pkeyline)!=0):pkeyline+=","
            pkeyline+=pk
        pkeys = pkeyline
    print('alter table %s add primary key(%s)'%(table,pkeys))
    engine.execute('alter table %s add primary key(%s)'%(table,pkeys))


def create_table(table_object):
    metadata = MetaData()
    metadata.create_all(engine)
    