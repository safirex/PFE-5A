from typing import Any
from importlib_metadata import metadata
from pandas import DataFrame
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.types import *
from enum import Enum
from files_format_enums import GTFSFilenames



class DbTables(Enum):
    ''' set a fixed way to access db tables '''
    Test = 1


uri = 'mysql://root:eudeseude@localhost:3306/pfe'
engine = create_engine(uri, echo=False)
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
    