from pandas import DataFrame
from sqlalchemy import MetaData, Table, select
import numpy as np
from db.dbConnection import *
from db.dbschemes import get_db_table_dtype, get_db_table_pkeys
from gtfs_parser import get_entity_column_names, get_stop_column_names 
metadata = MetaData()
engine = get_engine()
raw_character_data_format = Table('raw_character_info', metadata, autoload_with=engine)

s = select(raw_character_data_format)
result = DataFrame( engine.execute(s))
result = result.drop(0,axis=1) #remove colum of line numbers added by sql query

trip_columns = get_entity_column_names()[:-1]
stop_columns = get_stop_column_names()
column_names = trip_columns+stop_columns
print(column_names)


result = result.set_axis(column_names,axis=1) 
stop_info = result.drop(trip_columns[1:],axis=1)     # stop_id,arrival delay/time, departure delay/time
trip_info = result.drop(stop_columns,axis=1)     # stop_id,arrival delay/time, departure delay/time
# result = result.to_numpy()
# trip_info = DataFrame(result[:,:6])             # trip id, route id, direction, timestamp, vehicle id/label

print(trip_info,stop_info)




trip_table = "rt_trip_info"
stop_table = "rt_stop_info"

add_Data(DataFrame(trip_info),trip_table,dtype= get_db_table_dtype(GTFSFilenames.RT)['trip'])
add_Data(DataFrame(stop_info),stop_table,dtype= get_db_table_dtype(GTFSFilenames.RT)['stop'])
alter_table_add_pk(trip_table,get_db_table_pkeys(GTFSFilenames.RT)['trip'])
alter_table_add_pk(stop_table,get_db_table_pkeys(GTFSFilenames.RT)['stop'])

