import streamlit as st
import numpy as np
import pandas as pd
import datetime
# https://docs.streamlit.io/library/api-reference/widgets
import sys
sys.path.append("..")
import db.dbConnection as db
import data.data_fetcher as fd

col1, col2 = st.columns(2)
with col1:
    d = st.date_input(
        "begin date",
        datetime.date.today())
with col2:
    end = st.date_input(
        "end date",
        datetime.date.today())
st.write("data from ", d," to ",end)

engine = db.get_engine()

st.dataframe( data=fd.select_raw_data())

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)