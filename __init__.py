from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from logger import setup_logger
import config
from datetime import datetime
#from models import db, StationsModel

app = Flask(__name__)
 
logger = setup_logger(app)
app.config.from_object(config)

mysql = MySQL(app)

#временный метод, выводит список всех станций
@app.route('/')
def stations():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM stations')
    rows = cur.fetchall()
    cur.close

    # Преобразуем данные в словарь
    stations = []
    for row in rows:
        stations.append({
            'id': row[0],
            '1chip_id': row[1],
            'tetle': row[2]
        })
    
    return jsonify(stations)

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

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM stations WHERE 1chip_id = %s', (mac_id,))
    station = cur.fetchone()
    cur.close()

    #если такого mac_id нет, просто добавляем в таблицу, чтобы потом разобраться
    if not station:
        cur = mysql.connection.cursor()
        cur.execute('''
                INSERT INTO stations (1chip_id, title, latitude, longitude)
                VALUES (%s, %s, %s, %s)
            ''', (mac_id, 'test', 2, 3))

        station_id = cur.lastrowid

        mysql.connection.commit()
        cur.close()
    else:
        if isinstance(station, tuple):
            station_id = station[0]
        else:
            station_id = station.id

    cur = mysql.connection.cursor()
    cur.execute('''
            INSERT INTO station_data 
            (`station_id`, `timestamp`, `average_wind`, `min_wind`, `gusts`, `wind_direction`, `pressure`, `internal_temperature`, `external_temperature`, `humidity`, `precipitation`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (station_id, datetime.now(), params_vals['a'], params_vals['m'], params_vals['g'], params_vals['d5'], params_vals['p'], params_vals['tp'], params_vals['te2'], params_vals['h'], 0))
    
    mysql.connection.commit()
    cur.close()

    return jsonify({"msg": "Data saved!"})

def parseParams(param):
    try: 
        p = request.args.get(param)
        p = float(p)
        return p
    except Exception as e:
        raise ValueError(e)


if __name__ == '__main__':
    app.run(debug=True)
