# app.py
from flask import Flask
import psycopg2
import time

app = Flask(__name__)

def get_db_connection():
    # Optional: retry logic (not strictly needed if healthcheck works)
    conn = psycopg2.connect(
        host="postgres_db",
        database="mydb",
        user="myuser",
        password="mypassword"
    )
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT message FROM messages WHERE id = 1;')
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            message = row[0]
        else:
            message = "⚠️ No message found in DB"
    except Exception as e:
        message = f"❌ DB Error: {str(e)}"

    return f'''
    <html>
    <head><title>Flask + PostgreSQL</title></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1>Flask is running!</h1>
        <p><strong>Status:</strong> Connected to PostgreSQL</p>
        <h2>Message from database:</h2>
        <p><strong>{message}</strong></p>
        <hr>
        <small>Refresh page to see updated data from PostgreSQL.</small>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)