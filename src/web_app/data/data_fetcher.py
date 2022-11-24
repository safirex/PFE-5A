import sys
import pandas as pd
import time
import datetime
sys.path.append("../..")
import db.dbConnection as db
from  files_format_enums import GTFSFilenames as tables
from gtfs_parser import get_rt_column_names

engine = db.get_engine()

def select_raw_data():
    return pd.DataFrame( engine.execute('select * from raw_rt_data limit 100;'))

def select_rt_stops(begin,end):
    begin_date = date_to_timestamp(begin)
    end_date = date_to_timestamp(end)
    table = tables.rt_stop_info
    print("begins at ",begin_date)
    query = 'select * from '+ table.name +' where arrival_time>'+str(begin_date)+' and departure_time<'+str(end_date)
    res =  pd.DataFrame(engine.execute(query),columns=get_rt_column_names(table))

    # setup dataframe labels
    modify_rt_data_timestamp(res,'arrival_time')
    modify_rt_data_timestamp(res,'departure_time')
    return res

def select_scheduled_stops():
    table = tables.stop_times
    query = 'select * from ' + table.name + ';' 
    res =  pd.DataFrame(engine.execute(query),columns=['trip_id','arrival_time','departure_time','stop_id','stop_sequence',' pickup_type','drop_off_type'])
    res = res.drop(0)
    return res


def select_stop_rt_on_scheduled():
    column = get_rt_column_names(tables.rt_stop_info)+['static_arrival_time','static_departure_time']
    
    query = """ SELECT rt.*,st.arrival_time,st.departure_time FROM stop_times AS st
                INNER JOIN rt_stop_info rt
                ON st.trip_id = rt.trip_id AND st.stop_id = rt.stop_id
                LIMIT 1000; """
    
    res =  pd.DataFrame(engine.execute(query),columns=column)
    res = modify_rt_data_timestamp(res,'arrival_time')
    res = modify_rt_data_timestamp(res,'departure_time')
    return res

def select_rt_scheduled2():
    column = get_rt_column_names(tables.rt_stop_info)[:3]+['departure_delay','static_arrival_time','static_departure_time']
    query = """ SELECT rt.trip_id,rt.stop_id,ROUND(AVG(rt.arrival_delay)),ROUND(AVG(rt.departure_delay)),st.arrival_time,st.departure_time FROM stop_times AS st
                INNER JOIN rt_stop_info rt
                ON st.trip_id = rt.trip_id AND st.stop_id = rt.stop_id
                GROUP BY rt.trip_id,rt.stop_id,st.arrival_time  ; """
    
    res =  pd.DataFrame(engine.execute(query),columns=column)
    print("return of db = ",res)
    # res = modify_rt_data_timestamp(res,'arrival_time')
    # res = modify_rt_data_timestamp(res,'departure_time')
    return res

def date_to_timestamp(user_date:datetime.date):
    return time.mktime(datetime.datetime.strptime(str(user_date), "%Y-%m-%d").timetuple())

def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

def set_data_labels(data:pd.DataFrame,table:tables):
    columns = get_rt_column_names(table)
    print(columns)
    data.columns = columns

def modify_rt_data_timestamp(data:pd.DataFrame,colName:str):
    for i in range(len(data[colName])) :
        data[colName][i] = timestamp_to_date(data[colName][i])
    return data