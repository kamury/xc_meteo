from flask import jsonify, render_template, request
from .. import app
from .. import models

#добавляет данные с метеостанции или пишет ошибку в лог
@app.route('/add_data', methods=['GET'])
def add_station():

    #x - station code, mac_id 
    mac_id = request.args.get('x')

    if not (mac_id and mac_id.isalnum()):
        app.logger.info(f'Wrong value for station code(param x), request url: {request.url}')
        return jsonify({"error": "Wrong value for station code(param x)"}), 400 

    #получаем все остальные параметры
    params = ['a', 'm', 'g', 'd5', 'p', 'tp', 'te2', 'h'];
    req_params = ['a', 'm', 'g', 'd5'];
    params_vals = {}

    for i in params:
        try:
            params_vals[i] = parseParams(i)
        except Exception as e:
            if i in req_params:
                #если нет обязательного параметра, возвращаем ошибку и пишем в лог
                app.logger.info(f'Wrong value for param: {i}, request url: {request.url}')
                return jsonify({"error": f"Wrong value for param: {i}"}), 400
            else:
                params_vals[i] = None;

    #пересчитываем ветер в м/c
    params_vals['a'] = params_vals['a']/10
    params_vals['m'] = params_vals['m']/10
    params_vals['g'] = params_vals['g']/10

    #пересчитываем направление в градусы, исходное значение от 0 до 1024
    params_vals['d5'] = (params_vals['d5']/1024)*360

    station = models.get_station_by_mac_id(mac_id)

    #если такого mac_id нет, просто добавляем в таблицу, чтобы потом разобраться
    if not station:
        station_id = models.add_station(mac_id)
    else:
        station_id = station['id']

    models.add_station_data(station_id, params_vals)

    return jsonify({"msg": "Data saved!"})

def parseParams(param):
    try: 
        p = request.args.get(param)
        p = float(p)
        return p
    except Exception as e:
        raise ValueError(e)
