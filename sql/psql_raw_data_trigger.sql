

CREATE FUNCTION insert_trigger() RETURNS trigger AS $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM rt_trip_info WHERE trip_id = NEW.trip_id) THEN
        INSERT INTO rt_trip_info(trip_id,route_id,direction_id,timestamp,vehicle_id,vehicle_label)
        VALUES (    new.trip_id,new.route_id,new.direction_id,new.timestamp,new.vehicle_id,new.vehicle_label);
        END if;
        IF NOT EXISTS (SELECT 1 FROM rt_stop_info WHERE trip_id = NEW.trip_id AND stop_id = NEW.stop_id ) THEN
        INSERT INTO rt_stop_info(trip_id,stop_id,arrival_delay,arrival_time,departure_delay,departure_time,scheduled_relationship)
        VALUES ( new.trip_id,new.stop_id,new.arrival_delay,new.arrival_time,new.departure_delay,new.departure_time,NEW.scheduled_relationship);
        END if;
    END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER raw_rt_data_after_insert AFTER INSERT ON raw_rt_data FOR EACH ROW 
EXECUTE PROCEDURE insert_trigger();

