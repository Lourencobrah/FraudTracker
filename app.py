from flask import Flask, request, jsonify, render_template, make_response
import sqlite3
import datetime
import os

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
                        timestamp TEXT,
                        nome TEXT,
                        email TEXT,
                        telefone TEXT)''')  # Corrigido aqui, com a coluna telefone
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
@app.route('/track', methods=['POST'])
def track():
    try:
        data = request.json
        print(f"Dados recebidos: {data}")  # Imprime todos os dados para ver o que está sendo enviado

        ip = request.remote_addr
        latitude = data.get('latitude', 'Desconhecido')
        longitude = data.get('longitude', 'Desconhecido')
        user_agent = data.get('user_agent', 'Desconhecido')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nome = data.get('nome', 'N/A')
        email = data.get('email', 'N/A')
        telefone = data.get('telefone', 'N/A')

        # Verifica se todos os dados estão sendo recebidos corretamente
        print(f"IP: {ip}, Latitude: {latitude}, Longitude: {longitude}, User Agent: {user_agent}, Nome: {nome}, Email: {email}, Telefone: {telefone}")

        # Conexão com o banco de dados e inserção de dados
        conn = sqlite3.connect("fraud_tracker.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (ip, latitude, longitude, user_agent, timestamp, nome, email, telefone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (ip, latitude, longitude, user_agent, timestamp, nome, email, telefone))
        conn.commit()
        conn.close()

        return make_response(jsonify({"status": "sucesso", "message": "Dados registrados"}), 200)

    except Exception as e:
        print(f"Erro ao registrar dados: {e}")  # Imprime o erro se acontecer
        return make_response(jsonify({"status": "erro", "message": f"Erro ao registrar dados: {str(e)}"}), 500)

@app.route('/logs')
def view_logs():
    conn = sqlite3.connect("fraud_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall() 
    conn.close()

    return render_template('logs.html', logs=logs)

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    conn = sqlite3.connect("fraud_tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
    return jsonify({"status": "sucesso", "message": "Logs apagados"})


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 10000)) 
    app.run(host='0.0.0.0', port=port)
