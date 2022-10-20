from sqlalchemy import BIGINT, VARCHAR, Date, Integer, PrimaryKeyConstraint, Table, Text
import sys
sys.path.append('..')
from files_format_enums import *
from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, Boolean
from datetime import datetime

dtype_dict = {}
dtype_dict[GTFSFilenames.agency]            =  {"agency_id" : VARCHAR(50)}     
dtype_dict[GTFSFilenames.calendar]          =  {"service_id" :VARCHAR(50), 'start_date' : Date}   
dtype_dict[GTFSFilenames.calendar_dates]    =  {"service_id" :VARCHAR(50),"date" : Date}
dtype_dict[GTFSFilenames.routes]            =  {"route_id"  : VARCHAR(20)}      
dtype_dict[GTFSFilenames.shapes]            =  {"shape_id"  : VARCHAR(20),"shape_pt_sequence": Integer()} 
dtype_dict[GTFSFilenames.stops]             =  {"stop_id"   : VARCHAR(20)}     
dtype_dict[GTFSFilenames.stop_times]        =  {"stop_id"   : VARCHAR(20), "trip_id" :  VARCHAR(50)}      
dtype_dict[GTFSFilenames.trips]             =  { "trip_id"  : VARCHAR(50)} 



pk_dict = {}
pk_dict[GTFSFilenames.agency]            =  ["agency_id"]     
pk_dict[GTFSFilenames.calendar]          =  ["service_id","start_date"]    
pk_dict[GTFSFilenames.calendar_dates]    =  ["service_id","date"]    
pk_dict[GTFSFilenames.routes]            =  ["route_id"]      
pk_dict[GTFSFilenames.shapes]            =  ["shape_id","shape_pt_sequence"] 
pk_dict[GTFSFilenames.stops]             =  ["stop_id"]       
pk_dict[GTFSFilenames.stop_times]        =  ["stop_id","trip_id"]       
pk_dict[GTFSFilenames.trips]             =  ["trip_id"]       


def get_db_table_dtype(tablename :GTFSFilenames):
    return dtype_dict[tablename]
def get_db_table_pkeys(tablename :GTFSFilenames):
    return pk_dict[tablename]




metadata = MetaData()
trips_rt = Table('trips',metadata,
    Column('trip_id',VARCHAR(50),primary_key=True),
    Column('route_id',VARCHAR(50)),
    Column('direction_id',BIGINT),
    Column('timestamp',BIGINT,primary_key=True),
    Column('vehicle_id',VARCHAR(50)),
    Column('vehicle_label',VARCHAR(50)),
    Column('stop_id',VARCHAR(50),primary_key=True),
    Column('arrival_delay',BIGINT),
    Column('arrival_time',BIGINT),
    Column('arrival_delay',BIGINT),
    Column('departure_delay',BIGINT),
    Column('departure_time',BIGINT),
)

