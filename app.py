import sqlite3
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Vulnerabilidad 1: SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 401


# Vulnerabilidad 2: Command Injection
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')

    result = subprocess.check_output(
        f"ping -c 1 {host}",
        shell=True
    )

    return jsonify({"result": result.decode()})


# Vulnerabilidad 3: Debug habilitado
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
