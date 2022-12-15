import streamlit as st
import numpy as np
import pandas as pd
import datetime

import plotly.figure_factory as ff
import plotly.express as px
import charts.plotly as charts
import sys
sys.path.append("..")
# https://docs.streamlit.io/library/api-reference/widgets

import db.dbConnection as db
import data.data_fetcher as fd
from data.utils import *

data = {}
def fetch_data(line_limit,begin_date,end_date):
    # if(datetime.date.today()==end_date):
    #     # because end_date is a date without hour format
    #     end_date = datetime.datetime.now()
    data['stops'] = fd.select_stop_data()
    data['stop_names'] =data['stops'][['stop_id','stop_name']]
    print(data['stop_names'])
    data['stops_average_delay'] = fd.select_rt_scheduled2(line_limit, begin_date, end_date)
    data['scheduled_stops']=fd.select_scheduled_stops(line_limit)
    data['rt_stops'] = fd.select_rt_stops(line_limit, begin_date, end_date)
    data['stops_per_hour'] = fd.select_nb_stops_per_hour(line_limit,begin_date,end_date)


col1, col2 = st.columns(2)
with col1:
    begin_date = st.date_input(
        "begin date",
        datetime.datetime.now() - datetime.timedelta(days=32))
with col2:
    end_date = st.date_input(
        "end date",
        datetime.datetime.now())
line_limit = st.number_input("db line limit (0 = whole table)",value=1000,min_value=0,max_value=None)



'''# stops par heure'''

fetch_data(line_limit,begin_date,end_date)
tmp = data['stops_per_hour']
hist_data:pd.DataFrame = tmp[['stop_id','AVG(arrival_delay)','arrival_hour']]




# selection id et format graph en fonction

stop_labels:pd.DataFrame = data['stop_names'][['stop_name','stop_id']]
stop_labels = data['stop_names'][['stop_name','stop_id']]
col1,col2 = st.columns(2)






with col1:
    stop_label =st.selectbox('stop name to observe',np.unique(stop_labels['stop_name']))
    filter = stop_labels['stop_name'] == stop_label
    stop_line = stop_labels.where(filter).dropna()   
    
with col2:
    stop = st.selectbox('stop id to observe',stop_line['stop_id'])
    stop_data = hist_data.where(hist_data['stop_id']==stop)
    
st.write("données sur arret ",stop_label,stop, " du ", begin_date," au ",end_date)
'### délais moyen des véhicules par rapport aux horaires prévus selon les horaires de la journée'
fig = px.histogram(stop_data, x='arrival_hour',y='AVG(arrival_delay)',histfunc='avg')
st.plotly_chart(fig)


select_stop_data_r = fd.select_stops_by_id(str(stop),begin_date,end_date,True)
select_stop_data = select_stop_data_r.to_numpy()
work_hours = get_working_hours_stop(select_stop_data[:,5])
print("work hours = ",work_hours)
max_interval = select_stop_data[1,5] - select_stop_data[0,5] 
for i  in range(1,len(select_stop_data)):
    current_interval = select_stop_data[i,5] - select_stop_data[i-1,5]
    current_hour = math.floor(select_stop_data[i,5]/3600)
    not_first_hour_of_day = (current_hour-1)%24 in work_hours
    # check the interval isn't because it's night
    if(max_interval< current_interval and not_first_hour_of_day ): 
        max_interval = current_interval
max_interval = datetime.timedelta(seconds= max_interval)
print(max_interval)
# st.write("work hours %s"%work_hours)
st.write("l'attente maximal entre 2 vehicules sur ce stop est de  %s."%max_interval)

# nb arrets par heure

stops_per_id :pd.DataFrame= data['stops_per_hour'][['stop_id','arrival_hour','COUNT(*)']]
stops_per_id.columns = ['stop_id','arrival_hour','nb_stops']
time_duration = (pd.Timestamp(end_date) - pd.Timestamp(begin_date)).days
stop_names:pd.DataFrame = data['stop_names']
stop_names.columns = ['nom de stop','stop_id']
st.dataframe(stop_names)


stops_per_id['nb moyen de stops'] = stops_per_id.apply(lambda row: row.nb_stops /time_duration , axis = 1)
# st.dataframe(stops_per_id)

stops_per_id = stops_per_id.set_index('stop_id').join(stop_names.set_index('stop_id'))
print(stops_per_id)
# stops_per_id = stops_per_id.iloc[:,[3,0,1,2]]   # change column order

st.dataframe(stops_per_id)
