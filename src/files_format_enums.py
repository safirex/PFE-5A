
from enum import Enum


class GTFSFilenames(Enum):
    routes = 0
    agency    = 1
    calendar= 2
    calendar_dates =3
    shapes=4
    stop_times=5
    stops=6
    trips=7
    RT = 8
    rt_stop_info = 9
    rt_trip_info = 10
    raw_rt_data = 11