import streamlit as st
import numpy as np
import pandas as pd
import datetime
import plotly.figure_factory as ff
import plotly.express as px
# https://docs.streamlit.io/library/api-reference/widgets
import sys
sys.path.append("..")
import db.dbConnection as db
import data.data_fetcher as fd
import charts.plotly as charts

data = {}
def fetch_data(line_limit,begin_date,end_date):
    data['stops_average_delay'] = fd.select_rt_scheduled2(line_limit,begin_date,end_date)
    data['scheduled_stops']=fd.select_scheduled_stops()
    data['rt_stops'] = fd.select_rt_stops(begin_date,end_date)
    data['stops_per_hour'] = fd.select_nb_stops_per_hour()


col1, col2 = st.columns(2)
with col1:
    begin_date = st.date_input(
        "begin date",
        datetime.date.today())
with col2:
    end_date = st.date_input(
        "end date",
        datetime.date.today())
st.write("data from ", begin_date," to ",end_date)

line_limit = st.number_input("db line limit (0 = whole table)",value=1000,min_value=0,max_value=None)
sql_display = st.selectbox("display request based on ",('stop ids', 'station names'))


fetch_data(line_limit,begin_date,end_date)

engine = db.get_engine()

# st.dataframe( data=fd.select_raw_data())
# st.write("scheduled stops")
# st.dataframe(data['scheduled_stops'])
# st.write("rt stops")
# st.dataframe(data['rt_stops'])

# trip_ids = data['scheduled_stops']

st.dataframe(data['stops_average_delay'])


st.dataframe(data['stops_per_hour'])
tmp = data['stops_per_hour']
hist_data:pd.DataFrame = tmp[['stop_id','AVG(arrival_delay)','arrival_hour']]

# st.dataframe(hist_data)
st.write("retard moyen en seconde du réseau dijonnais au fil de la journée ")
fig = px.histogram(hist_data, x='arrival_hour',y='AVG(arrival_delay)',histfunc='avg')
st.plotly_chart(fig)

stop =st.selectbox('stop id to observe',hist_data['stop_id'])
print(hist_data.where(hist_data['stop_id']==stop))
stop_data = hist_data.where(hist_data['stop_id']==stop)
fig = px.histogram(stop_data, x='arrival_hour',y='AVG(arrival_delay)',histfunc='avg')
st.plotly_chart(fig)