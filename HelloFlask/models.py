from .db import query_db
from datetime import datetime

def get_all_stations():
    return query_db('SELECT * FROM stations')

def get_station_by_mac_id(mac_id):
    return query_db('SELECT * FROM stations WHERE mac_id = %s', [mac_id], one=True);

def get_station_by_id(id):
    return query_db('SELECT * FROM stations WHERE id = %s', [id], one=True);

def add_station(mac_id):
    return query_db(
        '''INSERT INTO stations (1chip_id,mac_id, title, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s)''',
        ["", mac_id, 'test', 3, 4]
    )

def get_station_data_per_page(station_id, page, per_page):
    return query_db('SELECT * FROM station_data WHERE station_id = %s ORDER BY timestamp DESC LIMIT %s OFFSET %s', [station_id, per_page, (page - 1)*per_page]);

def get_station_data_total_count(station_id):
    count = query_db('SELECT COUNT(*) as cnt FROM station_data WHERE station_id = %s', [station_id], one=True);
    return count['cnt']

def add_station_data(station_id, query):
    return query_db(
        '''INSERT INTO station_data 
            (`station_id`, `timestamp`, `average_wind`, `min_wind`, `gusts`, `wind_direction`, `pressure`, `internal_temperature`, `external_temperature`, `humidity`, `precipitation`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        [station_id, datetime.now(), query.average_wind, query.min_wind, query.gusts, query.wind_direction, query.p, query.tp, query.te2, query.h, query.pr]
    )