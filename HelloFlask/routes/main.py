from flask import render_template
from .. import app
from ..models import get_all_stations, get_station_by_id, get_station_data

@app.route('/')
def index():
    stations = get_all_stations()
    return render_template('index.html', stations=stations)

@app.route('/show_data/<int:station_id>')
def show_data(station_id):
    station = get_station_by_id(station_id)
    if station:
        data = get_station_data(station_id)
        print(data)
        return render_template('show_data.html', station=station, data=data)
    else:
        return render_template('wrong_station_id.html')    
    