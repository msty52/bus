import os
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Рекомендуется заменить порт 5432 на 6543 и добавить ?sslmode=require для стабильности в облаке
LOCAL_DB_URL = 'postgresql://postgres:ТВОЙ_ПАРОЛЬ@aws-0-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require'

uri = os.environ.get('DATABASE_URL') or LOCAL_DB_URL

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- МОДЕЛИ ДАННЫХ ---

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

class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    route_number = db.Column(db.String(10))
    start_point = db.Column(db.String(100))
    end_point = db.Column(db.String(100))

class Schedule(db.Model):
    __tablename__ = 'Schedules' # Имя таблицы в Supabase
    id = db.Column('номер', db.Integer, primary_key=True)
    bus_id = db.Column('номер автобуса', db.Integer, db.ForeignKey('buses.id'))
    route_id = db.Column('идентификатор маршрута', db.Integer, db.ForeignKey('routes.id'))
    departure_time = db.Column('время отправления', db.Time)
    stop_name = db.Column('Название остановки', db.String(100))

    # Связи для получения данных из соседних таблиц
    bus = db.relationship('Bus', backref='schedules')
    route = db.relationship('Route', backref='schedules')

# --- ГЛАВНАЯ СТРАНИЦА ---

@app.route('/')
def index():
    try:
        buses = Bus.query.all()
        drivers = Driver.query.all()
        schedules = Schedule.query.order_by(Schedule.departure_time).all()

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
                h1, h2 { color: #333; margin-top: 30px; }
                .status { color: green; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Управление Автобусным Парком</h1>
            
            <p class="status">✔ Подключено к базе данных Supabase</p>

            <h2>Расписание маршрутов (г. Твой Город)</h2>
            <table>
                <tr>
                    <th>Время</th>
                    <th>Маршрут</th>
                    <th>Автобус (Гос. номер)</th>
                    <th>Остановка</th>
                </tr>
                {% for item in schedules %}
                <tr>
                    <td>{{ item.departure_time.strftime('%H:%M') }}</td>
                    <td>{{ item.route.route_number }} ({{ item.route.start_point }} - {{ item.route.end_point }})</td>
                    <td>{{ item.bus.number_plate }}</td>
                    <td>{{ item.stop_name }}</td>
                </tr>
                {% endfor %}
            </table>

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
        </body>
        </html>
        """
        return render_template_string(template, buses=buses, drivers=drivers, schedules=schedules)
    
    except Exception as e:
        return f"<h1 style='color:red;'>Ошибка подключения к базе данных!</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)
