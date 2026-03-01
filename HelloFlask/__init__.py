from flask import Flask
from datetime import datetime
#from models import db, StationsModel

from .logger import setup_logger
from . import config, db, models

'''
app = Flask(__name__)
 
logger = setup_logger(app)
app.config.from_object(config)

mysql = MySQL(app)
'''


app = Flask(__name__)
app.config.from_object(config)

# Инициализируем MySQL с этим приложением
db.init_app(app)

from .routes import main, stations

'''
#временный метод, выводит список всех станций
@app.route('/')
def stations():
    stations = models.get_all_stations();
    return jsonify(stations)
'''