from sqlalchemy import BIGINT, INTEGER, VARCHAR, Column, MetaData, Table, create_engine

uri = 'mysql://root:eudeseude@localhost:3306/pfe'
engine = create_engine(uri, echo=False)
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
    Column('arrival_delay',BIGINT),
    Column('departure_delay',BIGINT),
    Column('departure_time',BIGINT),
)

metadata.create_all()