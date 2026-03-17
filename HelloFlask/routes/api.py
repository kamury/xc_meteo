from flask import jsonify, render_template, request
from flask_pydantic import validate
from flask_pydantic.exceptions import ValidationError
from pydantic import BaseModel, Field, computed_field
from typing import Optional
import traceback
from .. import app
from .. import models

class QueryModel(BaseModel):
    x: str = Field(pattern=r'^[a-zA-Z0-9]+$', description="mac_id")
    a: float = Field(..., description="Average wind")
    m: float = Field(..., description="Min wind")
    g: float = Field(..., description="Gusts")
    d5: float = Field(..., description="Wind direction")
    p: Optional[float] = Field(None, description="Давление в hPa")
    tp: Optional[float] = Field(None, description="Температура внутреннего датчика температуры")
    te2: Optional[float] = Field(None, description="Температура внешнего датчика температуры")
    h: Optional[float] = Field(None, description="Влажность")
    pr: Optional[float] = Field(None, description="Количество срабатываний датчика осадков")

    @computed_field
    def wind_direction(self) -> float:
        return (self.d5/1024)*360

    @computed_field
    def average_wind(self) -> float:
        return (self.a/10)

    @computed_field
    def min_wind(self) -> float:
        return (self.m/10)

    @computed_field
    def gusts(self) -> float:
        return (self.g/10)  

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    app.logger.info(f'Error: {e.query_params}, request url: {request.url}')
    return jsonify({
        "error": "Bad request",
        "code": 400,
        "message": str(e.query_params)
    }), 400

#добавляет данные с метеостанции или пишет ошибку в лог
@app.route('/add_data', methods=['GET'])
@validate()
def add_station(query: QueryModel):

    try:
        station = models.get_station_by_mac_id(query.x)

        #если такого mac_id нет, просто добавляем в таблицу, чтобы потом разобраться
        if not station:
            station_id = models.add_station(query.x)
        else:
            station_id = station['id']

        models.add_station_data(station_id, query)

        return jsonify({"msg": "Data saved!"})
    except Exception as e:
        error_traceback = traceback.format_exc()
        app.logger.info(f'Error: {e}')
        app.logger.info(f'Traceback: {error_traceback}')
        return jsonify({"error": f'Error: {e}'}),500

