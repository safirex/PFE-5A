def parse_entity(entity):
    """

    Returns
    -------
    (trip_info, trip_stops)
    """
    if entity.HasField('trip_update'):
        trip_update     = entity.trip_update
        vehicle         = trip_update.vehicle
        trip_id         = trip_update.trip.trip_id
        route_id        = trip_update.trip.route_id
        timestamp       = trip_update.timestamp
        direction_id    = trip_update.trip.direction_id

        
        vehicle         = trip_update.vehicle
        vehicle_id      = vehicle.id
        vehicle_label   = vehicle.label

        stop_time_update    = trip_update.stop_time_update
        stop_list = []
        for stop in stop_time_update:
            stop_list.append(parse_stop_update(stop))
        
    return [trip_id,route_id,direction_id,timestamp,vehicle_id,vehicle_label],stop_list
    

def parse_stop_update(stop_update):
    stop_id     = stop_update.stop_id

    arrival     = stop_update.arrival
    departure   = stop_update.departure

    arrival_delay   = arrival.delay
    arrival_time    = arrival.time

    departure_delay = departure.delay
    departure_time  = departure.time

    return [stop_id,arrival_delay,arrival_time,departure_delay,departure_time]

def get_entity_column_names():
    return ['trip_id','route_id','direction_id','timestamp','vehicle_id','vehicle_label','stop_list']
def get_stop_column_names():
    return ['stop_id','arrival_delay','arrival_time','departure_delay','departure_time']