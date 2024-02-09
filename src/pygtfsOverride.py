from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from datetime import date
import sys

import six
from sqlalchemy import and_
from sqlalchemy.sql.expression import select, join

from pygtfs.gtfs_entities import (Feed, Service, ServiceException, gtfs_required,
                            Translation, Stop, Trip, ShapePoint, _stop_translations,
                            _trip_shapes, gtfs_calendar, gtfs_all)
from . import feed
def append_feed(schedule, feed_filename, strip_fields=True,file = True
                chunk_size=5000, agency_id_override=None):

    if(file):
        fd = feed.Feed(feed_filename, strip_fields)
    else:
        fd = CSV()
    gtfs_tables = {}
    for gtfs_class in gtfs_all:
        print('Loading GTFS data for %s:' % gtfs_class)
        gtfs_filename = gtfs_class.__tablename__ + '.txt'

        try:
            # We ignore the feed supplied feed id, because we create our own
            # later.
            gtfs_tables[gtfs_class] = fd.read_table(gtfs_filename,
                                                    set(c.name for c in gtfs_class.__table__.columns) - {'feed_id'})
        except (KeyError, IOError):
            if gtfs_class in gtfs_required:
                raise IOError('Error: could not find %s' % gtfs_filename)

    if len(set(gtfs_tables) & gtfs_calendar) == 0:
        raise PygtfsException('Must have Calendar.txt or Calendar_dates.txt')

    # create new feed
    feed_entry = Feed(feed_name=fd.feed_name, feed_append_date=date.today())
    schedule.session.add(feed_entry)
    schedule.session.flush()
    feed_id = feed_entry.feed_id
    for gtfs_class in gtfs_all:
        if gtfs_class not in gtfs_tables:
            continue
        gtfs_table = gtfs_tables[gtfs_class]


        for i, record in enumerate(gtfs_table):
            if not record:
                # Empty row.
                continue

            try:
                instance = gtfs_class(feed_id=feed_id, **record._asdict())
            except:
                print("Failure while writing {0}".format(record))
                raise
            schedule.session.add(instance)
            if i % chunk_size == 0 and i > 0:
                schedule.session.flush()
                sys.stdout.write('.')
                sys.stdout.flush()
        print('%d record%s read for %s.' % ((i+1), '' if i == 0 else 's',
                                            gtfs_class))
    schedule.session.flush()
    schedule.session.commit()
    # load many to many relationships
    if Translation in gtfs_tables:
        print('Mapping translations to stops')
        q = (schedule.session.query(
                Stop.feed_id.label('stop_feed_id'),
                Translation.feed_id.label('translation_feed_id'),
                Stop.stop_id.label('stop_id'),
                Translation.trans_id.label('trans_id'),
                Translation.lang.label('lang'))
            .filter(Stop.feed_id==feed_id)
            .filter(Translation.feed_id==feed_id)
            .filter(Stop.stop_name==Translation.trans_id)
            )
        upd = _stop_translations.insert().from_select(
                ['stop_feed_id', 'translation_feed_id', 'stop_id', 'trans_id', 'lang'], q)
        schedule.session.execute(upd)
    if ShapePoint in gtfs_tables:
        print('Mapping shapes to trips')
        q = (schedule.session.query(
                Trip.feed_id.label('trip_feed_id'),
                ShapePoint.feed_id.label('shape_feed_id'),
                Trip.trip_id.label('trip_id'),
                ShapePoint.shape_id.label('shape_id'),
                ShapePoint.shape_pt_sequence.label('shape_pt_sequence'))
            .filter(Trip.feed_id==feed_id)
            .filter(ShapePoint.feed_id==feed_id)
            .filter(ShapePoint.shape_id==Trip.shape_id)
            )
        upd = _trip_shapes.insert().from_select(
                ['trip_feed_id', 'shape_feed_id', 'trip_id', 'shape_id', 'shape_pt_sequence'], q)
        schedule.session.execute(upd)
    schedule.session.commit()

    print('Complete.')
    return schedule
