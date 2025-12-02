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

def init_db():
    """Создаёт таблицу и вставляет тестовую запись (если ещё не существует)."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Создаём таблицу, если её нет
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    """)

    # Проверяем, есть ли уже запись
    cur.execute("SELECT COUNT(*) FROM messages;")
    count = cur.fetchone()[0]

    if count == 0:
        # Вставляем тестовое сообщение
        cur.execute("INSERT INTO messages (content) VALUES (%s);", ("Привет из PostgreSQL!",))

    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    try:
        # Инициализируем БД при первом запросе
        init_db()

        # Читаем сообщение из таблицы
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT content FROM messages ORDER BY id LIMIT 1;")
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            message = row[0]
            status = "✅ Подключение к БД и чтение данных — успешно"
            output = f"<h2>Сообщение из базы данных:</h2><p><strong>{message}</strong></p>"
        else:
            status = "⚠️ Подключение к БД успешно, но таблица пуста"
            output = ""

    except Exception as e:
        status = f"❌ Ошибка БД: {e}"
        output = ""

    return f"""
    <html>
    <head><title>Flask + PostgreSQL</title></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1>Flask работает!</h1>
        <p><strong>Статус:</strong> {status}</p>
        {output}
        <hr>
        <small>Обновите страницу, чтобы увидеть данные из PostgreSQL.</small>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)