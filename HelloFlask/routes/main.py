from flask import render_template
from .. import app
from ..models import get_all_stations

@app.route('/')
def index():
    stations = get_all_stations()
    print(stations)
    return render_template('index.html', stations=stations)