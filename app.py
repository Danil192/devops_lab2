# app.py
from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'db'),
        database='postgres',
        user=os.getenv('DATABASE_USER', 'postgres'),
        password=os.getenv('DATABASE_PASSWORD', 'postgres')
    )
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        conn.close()
        status = "✅ Подключение к БД успешно"
    except Exception as e:
        status = f"❌ Ошибка БД: {e}"
    return f"Flask работает! {status}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)