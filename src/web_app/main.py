import streamlit as st
import numpy as np
import pandas as pd
import datetime
# https://docs.streamlit.io/library/api-reference/widgets
import sys
sys.path.append("..")
import db.dbConnection as db
import data.data_fetcher as fd

data = {}
def fetch_data():
    data['scheduled_stops']=fd.select_scheduled_stops()
    data['rt_stops'] = fd.select_rt_stops(begin_date,end_date)


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
# if st.button('reload data',type='secondary'):
#     fetch_data()


fetch_data()

engine = db.get_engine()

# st.dataframe( data=fd.select_raw_data())
# st.write("scheduled stops")
# st.dataframe(data['scheduled_stops'])
# st.write("rt stops")
# st.dataframe(data['rt_stops'])

# trip_ids = data['scheduled_stops']


st.dataframe(fd.select_rt_scheduled2())