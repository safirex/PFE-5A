from sqlalchemy import BIGINT, INTEGER, VARCHAR, Column, MetaData, Table, DateTime,create_engine

from db.dbConnection import get_engine



# crontab -e
engine = get_engine()
metadata = MetaData(engine)

raw_rt = Table('raw_rt_data',metadata,
    Column('id', INTEGER, primary_key=True,autoincrement='auto' ),
    Column('trip_id',VARCHAR(50)),
    Column('route_id',VARCHAR(50)),
    Column('direction_id',BIGINT),
    Column('timestamp',BIGINT),
    Column('vehicle_id',VARCHAR(50)),
    Column('vehicle_label',VARCHAR(50)),
    Column('stop_id',VARCHAR(50)),
    Column('arrival_delay',BIGINT),
    Column('arrival_time',BIGINT),
    Column('departure_delay',BIGINT),
    Column('departure_time',BIGINT),
    Column('scheduled_relationship',VARCHAR(50))
)


trips_rt = Table('rt_trip_info',metadata,
    Column('trip_id',VARCHAR(50),primary_key=True),
    Column('route_id',VARCHAR(50)),
    Column('direction_id',BIGINT),
    Column('timestamp',DateTime,primary_key=True),
    Column('vehicle_id',VARCHAR(50)),
    Column('vehicle_label',VARCHAR(50))
)

stop_rt = Table('rt_stop_info',metadata,
    Column('trip_id',VARCHAR(50),primary_key=True),
    Column('stop_id',VARCHAR(50),primary_key=True),
    Column('arrival_delay',BIGINT),
    Column('arrival_time',DateTime),
    Column('departure_delay',BIGINT,primary_key=True),
    Column('departure_time',DateTime),
    Column('scheduled_relationship',VARCHAR(50))
)

f = open("../sql/psql_raw_data_trigger.sql", "r")
trigger = f.read() 

# trigger = '''CREATE TRIGGER `raw_rt_data_after_insert` AFTER INSERT ON `raw_rt_data` FOR EACH ROW BEGIN
# IF NOT EXISTS (SELECT 1 FROM rt_trip_info WHERE trip_id = NEW.trip_id) THEN
# INSERT INTO rt_trip_info(trip_id,route_id,direction_id,timestamp,vehicle_id,vehicle_label)
# VALUES (    new.trip_id,new.route_id,new.direction_id,new.timestamp,new.vehicle_id,new.vehicle_label);
# END if;

# IF NOT EXISTS (SELECT 1 FROM rt_stop_info WHERE trip_id = NEW.trip_id AND stop_id = NEW.stop_id ) THEN
# INSERT INTO rt_stop_info(trip_id,stop_id,arrival_delay,arrival_time,departure_delay,departure_time,scheduled_relationship)
# VALUES ( new.trip_id,new.stop_id,new.arrival_delay,new.arrival_time,new.departure_delay,new.departure_time,NEW.scheduled_relationship);
# END if;

# END'''
metadata.create_all()
engine.execute(trigger)