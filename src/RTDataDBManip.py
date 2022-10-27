from pandas import DataFrame
from sqlalchemy import MetaData, Table, select
import numpy as np
from db.dbConnection import *
from db.dbschemes import create_tables, get_db_table_dtype, get_db_table_pkeys, get_table_schema
from gtfs_parser import get_entity_column_names, get_stop_column_names 
metadata = MetaData()
engine = get_engine()
raw_character_data_format = Table('raw_rt_data', metadata, autoload_with=engine)

s = select(raw_character_data_format)
result = DataFrame( engine.execute(s))

trip_columns = get_entity_column_names()[:-1]
stop_columns = get_stop_column_names()
column_names = trip_columns+stop_columns
print(column_names)
print(result)
result = result.drop(0,axis=1)                 # remove index column of raw data table
result = result.set_axis(column_names,axis=1) 
stop_info = result.drop(trip_columns[1:],axis=1) # stop_id,arrival delay/time, departure delay/time
trip_info = result.drop(stop_columns,axis=1)     # trip_id,route_id,direction_id,timestamp,vehicle_id,vehicle_label


print(trip_info,stop_info)

def create_rt_data_tables():
    """ create the tables for checked data """
    create_tables()

trip_table = "rt_trip_info"
stop_table = "rt_stop_info"


def rt_insert(dataframe:DataFrame,table_name,dtype=None):
    get_engine()
    dataframe.to_sql(
        table_name,
        engine,
        dtype = dtype,
        index=False,
        chunksize=1,
        if_exists='append',
    )
    engine.execute
    print("success")

# engine = get_engine()
# for index, row  in trip_info.iterrows():
#     print(row['trip_id'])
#     engine.execute('INSERT INTO %s(v_mn) VALUES ("%s")', row['V_MN'])


print(trip_info)


try: 
    
    rt_insert(trip_info,trip_table,dtype= get_db_table_dtype(GTFSFilenames.RT)['trip'])
except BaseException as err:
    print(err)


    
try:
    rt_insert(stop_info,stop_table,dtype= get_db_table_dtype(GTFSFilenames.RT)['stop'])
except BaseException as err:
    print(err)
# alter_table_add_pk(trip_table,get_db_table_pkeys(GTFSFilenames.RT)['trip'])
# alter_table_add_pk(stop_table,get_db_table_pkeys(GTFSFilenames.RT)['stop'])
