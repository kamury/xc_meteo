from .db import query_db
from datetime import datetime

def get_all_stations():
    return query_db('SELECT * FROM stations')

def get_station_by_mac_id(mac_id):
    return query_db('SELECT * FROM stations WHERE mac_id = %s', [mac_id], one=True);

def add_station(mac_id):
    return query_db(
        '''INSERT INTO stations (1chip_id,mac_id, title, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s)''',
        ["", mac_id, 'test', 3, 4]
    )

def get_station_data(mac_id):
    return query_db()

def add_station_data(station_id, params_vals):
    return query_db(
        '''INSERT INTO station_data 
            (`station_id`, `timestamp`, `average_wind`, `min_wind`, `gusts`, `wind_direction`, `pressure`, `internal_temperature`, `external_temperature`, `humidity`, `precipitation`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        [station_id, datetime.now(), params_vals['a'], params_vals['m'], params_vals['g'], params_vals['d5'], params_vals['p'], params_vals['tp'], params_vals['te2'], params_vals['h'], 0]
    )