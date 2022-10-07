import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

from db.dbConnection import *

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

file = open('gtfs-rt.txt', 'w') #write byte
# file = open('data.gtfs', 'w') 
for line in liste:
    file.write(line)
file.close()

# print(type(entity.trip_update.trip))
# print(entity.trip_update.trip)

# print(buses_dict['entity'][0])
df = pd.DataFrame(buses_dict['entity'][0])

engine,conn = connect(DbTables.Test)
  
def add_Data(dataframe,engine):
    dataframe.to_sql(
        'raw_character_info',
        engine,
        if_exists='append',
        dtype={
            "id" : Text,
            "trip_update" : JSON
        }
    )
    engine.execute


# df.to_sql('trip_update',con=conn)
# add_Data(df,engine)

print(df)
print(df['trip_update']['vehicle']['id'])
