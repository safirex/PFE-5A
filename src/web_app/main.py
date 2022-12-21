import streamlit as st
import numpy as np
import pandas as pd
import datetime
import plotly.figure_factory as ff
import plotly.express as px
import math
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
# sql_display = st.selectbox("display request based on ",('stop ids', 'station names'))

fetch_data(line_limit,begin_date,end_date)

engine = db.get_engine()

st.dataframe(data['stops_average_delay'])


st.dataframe(data['stops_per_hour'])
tmp = data['stops_per_hour']
hist_data:pd.DataFrame = tmp[['stop_id','AVG(arrival_delay)','arrival_hour']]

# st.dataframe(hist_data)
st.write("### retard moyen en seconde du réseau dijonnais au fil de la journée ")
fig = px.histogram(hist_data, x='arrival_hour',y='AVG(arrival_delay)',histfunc='avg')
st.plotly_chart(fig)







