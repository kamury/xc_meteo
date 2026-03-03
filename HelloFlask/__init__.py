from flask import Flask
from datetime import datetime
#from models import db, StationsModel

from .logger import setup_logger
from . import config, db, models

app = Flask(__name__)
app.config.from_object(config)

# Инициализируем MySQL с этим приложением
db.init_app(app)

from .routes import main, api