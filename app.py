from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres_db",
        database="mydb",
        user="myuser",
        password="mypassword"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT message FROM messages WHERE id = 1;')
    message = cur.fetchone()[0]
    cur.close()
    conn.close()

    return f'''
    <html>
    <head><title>Flask + PostgreSQL</title></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1>Flask is running!</h1>
        <p><strong>Status:</strong> ✅ Connected to DB and reading data successfully</p>
        <h2>Message from database:</h2>
        <p><strong>{message}</strong></p>
        <hr>
        <small>Refresh page to see updated data from PostgreSQL.</small>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)