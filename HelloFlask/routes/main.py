from flask import jsonify, render_template, request
from .. import app
from ..models import get_all_stations, get_station_by_id, get_station_data_per_page, get_station_data_total_count
from ..config import ITEMS_PER_PAGE
import traceback
import math


@app.route('/')
def index():
    try:
        stations = get_all_stations()
        return render_template('index.html', stations=stations)
    except Exception as e:
        app.logger.info(f'Error: {e}')
        return jsonify({"error": f'Error: {e}'}),500

@app.route('/show_data/<int:station_id>')
def show_data(station_id):
    try:
        page = request.args.get('page', 1, type=int)

        station = get_station_by_id(station_id)
        if station:
            total_count = get_station_data_total_count(station_id)
            total_pages = math.ceil(total_count / ITEMS_PER_PAGE)
            data = get_station_data_per_page(station_id, page, ITEMS_PER_PAGE)
            return render_template('show_data.html', station=station, data=data, page=page, total_pages = total_pages)
        else:
            return render_template('wrong_station_id.html')  
    except Exception as e:
        error_traceback = traceback.format_exc()
        app.logger.info(f'Error: {e}')
        app.logger.info(f'Traceback: {error_traceback}')
        return jsonify({"error": f'Error: {e}'}),500
        