import streamlit as st
import numpy as np
import pandas as pd
import datetime
import plotly.figure_factory as ff
import plotly.express as px
import math
# https://docs.streamlit.io/library/api-reference/widgets
import sys
sys.path.append("..")
import db.dbConnection as db
import data.data_fetcher as fd
import charts.plotly as charts

data = {}
def fetch_data(line_limit,begin_date,end_date):
    # if(datetime.date.today()==end_date):
    #     # because end_date is a date without hour format
    #     end_date = datetime.datetime.now()
    
    data['stops_average_delay'] = fd.select_rt_scheduled2(line_limit, begin_date, end_date)
    data['scheduled_stops']=fd.select_scheduled_stops(line_limit)
    data['rt_stops'] = fd.select_rt_stops(line_limit, begin_date, end_date)
    data['stops_per_hour'] = fd.select_nb_stops_per_hour(line_limit)


col1, col2 = st.columns(2)
with col1:
    begin_date = st.date_input(
        "begin date",
        datetime.datetime.now() - datetime.timedelta(days=32))
with col2:
    end_date = st.date_input(
        "end date",
        datetime.datetime.now())
col1, col2 = st.columns(2)
with col1:
    st.write("data from ", begin_date," to ",end_date)
with col2:
    pass
    # st.download_button("download csv from db data",help='dowload date from %s to %s'%(begin_date,end_date), data=fd.download_csv(begin_date,end_date))
line_limit = st.number_input("db line limit (0 = whole table)",value=1000,min_value=0,max_value=None)
sql_display = st.selectbox("display request based on ",('stop ids', 'station names'))


fetch_data(line_limit,begin_date,end_date)

engine = db.get_engine()


st.dataframe(data['stops_average_delay'])


st.dataframe(data['stops_per_hour'])
tmp = data['stops_per_hour']
hist_data:pd.DataFrame = tmp[['stop_id','AVG(arrival_delay)','arrival_hour']]

# st.dataframe(hist_data)
st.write("retard moyen en seconde du réseau dijonnais au fil de la journée ")
fig = px.histogram(hist_data, x='arrival_hour',y='AVG(arrival_delay)',histfunc='avg')
st.plotly_chart(fig)

stop =st.selectbox('stop id to observe',hist_data['stop_id'])
stop_data = hist_data.where(hist_data['stop_id']==stop)
fig = px.histogram(stop_data, x='arrival_hour',y='AVG(arrival_delay)',histfunc='avg')
st.plotly_chart(fig)


select_stop_data = fd.select_stops_by_id(str(stop),begin_date,end_date)
print(select_stop_data)
select_stop_data = select_stop_data.to_numpy()

max_interval = select_stop_data[1,5] - select_stop_data[0,5] 
for i  in range(1,len(select_stop_data)):
    current_interval = select_stop_data[i,5] - select_stop_data[i-1,5]
    ignore_night = math.floor(select_stop_data[i,5]/3600)>=5 and math.floor(select_stop_data[i-1,5]/3600)<3
    ignore_db_holes = math.floor(select_stop_data[i,5]/(3600*24)) - math.floor(select_stop_data[i-1,5]/(3600*24)) <1
    
    if(max_interval< current_interval and ignore_night):
        max_interval = current_interval
max_interval = datetime.timedelta(seconds= max_interval)
print(max_interval)

st.write("l'attente maximal sur ce stop est de  %s."%max_interval)