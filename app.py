import os
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- НАСТРОЙКА БАЗЫ ДАННЫХ ---

# Проверяем, есть ли переменная окружения DATABASE_URL (на Render/GitHub).
# Если её нет (запуск локально), используем твою строку напрямую.
# ВНИМАНИЕ: Замени 'ТВОЙ_ПАРОЛЬ' на реальный пароль от Supabase ниже.
LOCAL_DB_URL = 'postgresql://postgres:ТВОЙ_ПАРОЛЬ@db.kzgtonlqmkcvlhcshmgp.supabase.co:5432/postgres'

uri = os.environ.get('DATABASE_URL') or LOCAL_DB_URL

# Небольшой фикс для SQLAlchemy: он требует, чтобы строка начиналась с postgresql://, 
# а некоторые сервисы выдают postgres://
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- МОДЕЛИ ДАННЫХ (Таблицы из БД) ---

class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(20), unique=True, nullable=False)
    model = db.Column(db.String(50))
    capacity = db.Column(db.Integer)

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer)

# --- МАРШРУТЫ (Страницы сайта) ---

@app.route('/')
def index():
    try:
        # Запрашиваем данные из облачной базы
        buses = Bus.query.all()
        drivers = Driver.query.all()

        # HTML-шаблон прямо в коде для простоты (в курсовой лучше делать отдельный файл)
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Автобусный Парк</title>
            <style>
                body { font-family: sans-serif; margin: 40px; background-color: #f4f4f9; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 30px; background: white; }
                th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
                th { background-color: #3e52d5; color: white; }
                h1, h2 { color: #333; }
            </style>
        </head>
        <body>
            <h1>Управление Автобусным Парком</h1>
            
            <h2>Список автобусов</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Гос. номер</th>
                    <th>Модель</th>
                    <th>Вместимость</th>
                </tr>
                {% for bus in buses %}
                <tr>
                    <td>{{ bus.id }}</td>
                    <td>{{ bus.number_plate }}</td>
                    <td>{{ bus.model }}</td>
                    <td>{{ bus.capacity }}</td>
                </tr>
                {% endfor %}
            </table>

            <h2>Наши водители</h2>
            <ul>
                {% for driver in drivers %}
                <li>{{ driver.full_name }} (Стаж: {{ driver.experience }} лет)</li>
                {% endfor %}
            </ul>
            
            <p style="color: green;">✔ Подключено к базе данных Supabase</p>
        </body>
        </html>
        """
        return render_template_string(template, buses=buses, drivers=drivers)
    
    except Exception as e:
        return f"<h1 style='color:red;'>Ошибка подключения к базе данных!</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    # На локальном компьютере сайт будет доступен по адресу http://127.0.0.1:5000
    app.run(debug=True)
