import sys
import pandas as pd
import time
import datetime
from sqlalchemy import select
sys.path.append("../..")

import db.dbConnection as db
from  files_format_enums import GTFSFilenames as tables
from gtfs_parser import get_rt_column_names

engine = db.get_engine()

def select_raw_data():
    return pd.DataFrame( engine.execute('select * from raw_rt_data limit 100;'))

def select_rt_stops(line_limit,begin,end):
    begin_date = date_to_timestamp(begin)
    end_date = date_to_timestamp(end)
    limit = manage_line_limit(line_limit)
    table = tables.rt_stop_info
    query = 'select * from '+ table.name +' where arrival_time>'+str(begin_date)+' and departure_time<'+str(end_date)+' '+limit
    res =  pd.DataFrame(engine.execute(query),columns=get_rt_column_names(table))

    # setup dataframe labels
    modify_rt_data_timestamp(res,'arrival_time')
    modify_rt_data_timestamp(res,'departure_time')
    return res

def select_nb_stops_per_hour(line_limit,begin_date,end_date):
    # SELECT stop_id,AVG(arrival_delay),round(AVG(departure_delay)),cast(floor(arrival_time/3600) as INTEGER )%24 as hourly, COUNT(*) FROM rt_stop_info GROUP BY stop_id, hourly LIMIT 1000;
    table = tables.rt_stop_info.name
    limit = manage_line_limit(line_limit)
    when = manage_time_limit(begin_date,end_date,'arrival_time',True)
    columns = 'stop_id,AVG(arrival_delay),round(AVG(departure_delay)),MOD(cast(floor(arrival_time/3600) as INTEGER ) , 24) as arrival_hour,COUNT(*)'
    group = "group by stop_id, arrival_hour"
    query = '''select %s from %s where %s %s %s'''%(columns,table,when,group,limit)
    columns_name = columns.split(',')
    columns_name[-2] = 'arrival_hour'
    columns_name.pop(-3) 
    df= pd.DataFrame(engine.execute(query),columns=columns_name)
    df['round(AVG(departure_delay))']  =df['round(AVG(departure_delay))'].astype(int)
    df['AVG(arrival_delay)']  =df['AVG(arrival_delay)'].astype(int)
    return df
    


def select_scheduled_stops(limit:int):
    table = tables.stop_times
    query = 'select * from %s %s'%(table.name, manage_line_limit(limit))
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

def select_rt_scheduled2(line_limit:int,begin:datetime.datetime,end:datetime.datetime):
    date_condition = manage_time_limit(begin,end,'rt.arrival_time',True)
    limit_string = manage_line_limit(line_limit)
    sql_where = manage_sql_optional_conditions([date_condition])
    column = ['nom de stop','stop id','avg arrival delay','avg departure delay','count(*)']
    
    query = """ SELECT stops.stop_name,rt.stop_id,ROUND(AVG(rt.arrival_delay)),ROUND(AVG(rt.departure_delay)),count(*) FROM stop_times AS st
                INNER JOIN rt_stop_info rt
                ON st.trip_id = rt.trip_id AND st.stop_id = rt.stop_id
                INNER JOIN stops
                ON rt.stop_id = stops.stop_id
                """ + sql_where + """
                GROUP BY rt.stop_id,stops.stop_name
                """+ limit_string +"""; """
    
    res =  pd.DataFrame(engine.execute(query),columns=column)
    res['avg arrival delay']  =res['avg arrival delay'].astype(int)
    res['avg departure delay']  =res['avg departure delay'].astype(int)
    return res

def select_stop_data():
    query = "select * from " + tables.stops.name
    columns = ['stop_id','stop_code','stop_name', 'latitude','longitude','wheelchair boarding']
    return pd.DataFrame(engine.execute(query),columns=columns)
                        




















def download_csv(begin, end) :
    '''returns a zip file of 2 csv in binary format'''   
    test = {}
    test[tables.rt_stop_info] = "where "+manage_time_limit(begin,end,'arrival_time',True)
    test[tables.rt_trip_info] = "where "+manage_time_limit(begin,end,'timestamp',True)
    res=[]
    for table in test:
        query = """ select * from %s %s """%(table.name,test[table])
        df = pd.DataFrame(engine.execute(query),columns=get_rt_column_names(table))
        res.append(df.to_csv(index=False).encode('utf-8'))
        
    return [csv for csv in res]
    
def select_stops_by_id(id:str,begin,end, order_by_timestamp = False):
    when = manage_time_limit(begin,end,'departure_time',True)
    _,who = name_or_id(id,'id')
    where = manage_sql_optional_conditions([when,who])
    order = ("order by departure_time" if order_by_timestamp else "")
    query = "select * from %s %s %s"%(tables.rt_stop_info.name,where,order)    
    return pd.DataFrame(engine.execute(query))

def select_stops_by_name(name:str,begin,end):
    when = manage_time_limit(begin,end,'departure_time',True)
    join,who = name_or_id(name,'name')
    where = manage_sql_optional_conditions([when,who])
    query = "select stop_name,rt.* from %s %s %s"%(tables.rt_stop_info.name,join,where)    
    return pd.DataFrame(engine.execute(query))

def name_or_id(name_id:str, colum= 'name' or 'id') :
    if(colum=='id'):
        return "","stop_id = '%s'"%name_id
    elif(colum=='name'):
        return "rt inner join %s sc on rt.stop_id = sc.stop_id"%tables.stops.name, \
                    "stop_name like %s"%name_id
    raise BaseException("bad arguments")
def manage_line_limit(limit:int):
    limit_string =""
    if(limit!=0):
        limit_string = "limit "+str(limit)
    return limit_string

def manage_sql_optional_conditions(conditions:list,having=False):
    not_empty_conds = []
    for condition in conditions:
        if condition != "":
            not_empty_conds.append(condition)
    
    if(len(not_empty_conds)==0):
        return ""
    
    if(having): res = "having "
    else :      res = "where "

    for i in  range(len(not_empty_conds)):
        res = res + not_empty_conds[i]+" "
        if(i < len(not_empty_conds)-1):
            res = res + " and "
    return res


def manage_time_limit(begin:datetime.datetime, end:datetime.datetime, column:str, isTimestamp=False):
    '''
    isTimestamp : correspond to the format of the column refered to in the db 
    '''
    if(not isTimestamp):
        string = " %s > %s and %s < %s" %(column,str(begin),column,str(end))
    else:
        string = " %s > %d and %s < %d" %(column,date_to_timestamp(begin),column,date_to_timestamp(end))
    return string

def date_to_timestamp(user_date:datetime.date or datetime.datetime):
    return time.mktime(datetime.datetime.strptime(str(user_date), "%Y-%m-%d").timetuple())

def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

def set_data_labels(data:pd.DataFrame,table:tables):
    columns = get_rt_column_names(table)
    data.columns = columns

def modify_rt_data_timestamp(data:pd.DataFrame,colName:str):
    for i in range(len(data[colName])) :
        data[colName][i] = timestamp_to_date(data[colName][i])
    return data