from flask import Flask, jsonify
from flask_mysqldb import MySQL
#from models import db, StationsModel

app = Flask(__name__)

app.config['MYSQL_USER'] = "whitew42_meteo"
app.config['MYSQL_PASSWORD'] = "msbdFL=18L"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_DB'] = "whitew42_meteo"
 
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
    #x = request.args.get('x')
    #d5 = request.args.get('d5')

    #print('xx')
    data = []
    data.append({
            'x': 5,
            'd5':6
            })
    return jsonify(data)
    #return jsonify({"aa":"bb"})


if __name__ == '__main__':
    app.run()
