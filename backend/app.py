import time
import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'tasksdb')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'secret')

def get_db_connection():
    #Tenta di connettersi al database (retry)
    retries = 10
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError as e:
            print(f"Database non ancora pronto, riprovo in 2 secondi... ({retries} tentativi rimasti)")
            retries -= 1
            time.sleep(2)
    raise Exception("Impossibile connettersi al database PostgreSQL.")

def init_db():
    #Crea la tabella se, all'avvio, non esiste
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()
    print("Database inizializzato con successo.")

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, title FROM tasks ORDER BY id DESC;')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'id': t[0], 'title': t[1]} for t in tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'title' not in data or not data['title'].strip():
        return jsonify({'error': 'Il titolo del task è obbligatorio'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (title) VALUES (%s) RETURNING id, title;', (data['title'].strip(),))
        new_task = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': new_task[0], 'title': new_task[1]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s;', (task_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Task eliminata con successo'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)