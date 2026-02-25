from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import config
import time
#from models import db, StationsModel

app = Flask(__name__)
 
app.config.from_object(config)

mysql = MySQL(app)

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

@app.route('/add_data', methods=['GET'])
def add_station():

    #station code 
    x = request.args.get('x')

    if not (x and x.isalnum()):
        return jsonify({"error": "Wrong value for station code(param x)"}), 400 
        #return jsonify({"error": "Wrong value for station code(param x)"})


    #d5 - direction, from 0 to 1024
    try: 
        d5 = request.args.get('d5')
        d5 = float(d5)
        d5 = (d5/1024)*360
    except Exception as e:
         return jsonify({"error": "Wrong value for direction(param d5)"}), 400

    #p - pressure, hPa
    try: 
        p = request.args.get('p')
        p = float(p)
    except Exception as e:
         return jsonify({"error": "Wrong value for pressure(param p)"}), 400


    #tp, te2  - temperature
    #try 
    #    p = request.args.get('p')
    #    p = float(p)
    #except Exception as e:
    #     return jsonify({"error": "Wrong value for pressure(param p)"}), 400

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM stations WHERE 1chip_id = %s', (x,))
    station = cur.fetchone()
    cur.close()

    if station is None:
        cur = mysql.connection.cursor()
        cur.execute('''
                INSERT INTO stations (1chip_id, title, latitude, longitude)
                VALUES (%s, %s, %s, %s)
            ''', (x, 'test', 2, 3))

        station_id = cur.lastrowid

        mysql.connection.commit()
        cur.close()
    else:
        station_id = station.id

    cur = mysql.connection.cursor()
    cur.execute('''
            INSERT INTO station_data (station_id, timestamp, wind_direction, pressure, temperature, average_wind, min_wind, gusts, humidity, precipitation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (station_id, int(time.time()), d5, p, 11, 1, 1, 1, 1, 1))
    
    mysql.connection.commit()
    cur.close()

    #data = []
    #data.append({
    #        'x': x,
    #        'd5': 8
    #        })
    #return jsonify(data)
    return jsonify({"msg": "Data saved!"})


if __name__ == '__main__':
    app.run(debug=True)
