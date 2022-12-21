import streamlit as st
import datetime
import data.data_fetcher as fd

from  files_format_enums import GTFSFilenames as tables


col1, col2 = st.columns(2)
with col1:
    begin_date = st.date_input(
        "begin date",
        datetime.datetime.now() - datetime.timedelta(days=32))
with col2:
    end_date = st.date_input(
        "end date",
        datetime.datetime.now())

st.write("data from ", begin_date," to ",end_date)
col1, col2,col3 = st.columns(3)
with col1:
    # [trip,stop,raw] = fd.download_csv(begin_date,end_date)
    st.download_button("download csv of rt trips",
                        help='dowload data from %s to %s'%(begin_date,end_date), 
                        data=fd.download_csv(tables.rt_trip_info,begin_date,end_date),
                        mime="text/csv",
                        key='download-trips',
                        file_name="Divia-rt-trips-%s-to-%s"%(begin_date,end_date)
                    )
with col2:
    st.download_button("download csv of rt stops",
                        help='dowload data from %s to %s'%(begin_date,end_date), 
                        data=fd.download_csv(tables.rt_stop_info,begin_date,end_date),
                        mime="text/csv",
                        key='download-stops',
                        file_name="Divia-rt-stops-%s-to-%s"%(begin_date,end_date)
                    )
with col3:
    st.download_button("download csv of raw data",
                        help='dowload data from %s to %s'%(begin_date,end_date), 
                        data=fd.download_csv(tables.raw_rt_data,begin_date,end_date),
                        mime="text/csv",
                        key='download-raw',
                        file_name="Divia-rt-raw-%s-to-%s"%(begin_date,end_date)
                    )