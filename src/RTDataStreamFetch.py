from msilib import add_data
import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

from db.dbConnection import *
import gtfs_parser

# import pygtfs
# sched = pygtfs.Schedule(":memory:")
# pygtfs.append_feed(sched, "data.zip")  

#  https://mayors-ic.github.io/examples/gtfs-example.html


feed = gtfs_realtime_pb2.FeedMessage()
url = "https://proxy.transport.data.gouv.fr/resource/divia-dijon-gtfs-rt-trip-update"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
response = requests.get(url, headers=headers)
feed.ParseFromString(response.content)
buses_dict = protobuf_to_dict(feed)
liste = []
for entity in feed.entity:
    if entity.HasField('trip_update'):
        liste.append(str(entity.trip_update))

file = open('gtfs-rt.txt', 'w') 
for line in liste:
    file.write(line)
file.close()


engine,conn = connect(DbTables.Test)
  
def add_Data(dataframe,engine):
    dataframe.to_sql(
        'raw_character_info',
        engine,
        if_exists='append',
        dtype={
            "stop_id" : Text
        }
    )
    engine.execute

liste = []
for entity in feed.entity:
    if entity.HasField('trip_update'):

        liste.append(gtfs_parser.parse_entity(entity))
        # trip,trip_stops = gtfs_parser.parse_entity(entity)

def format_for_sql(gtfsrt_dict):
    trip_list = []
    for trip in gtfsrt_dict:
        infos = trip[:-1][0]
        trip_stops = trip[-1]

        for i in range (len(trip_stops)):
            trip_stops[i] = infos + trip_stops[i]
            trip_list.append(trip_stops[i] )
    col_names = gtfs_parser.get_entity_column_names()[:-1]+ gtfs_parser.get_stop_column_names()
    return pd.DataFrame(trip_list,columns=col_names)

df = format_for_sql(liste)

add_Data(df,engine)
print(df)