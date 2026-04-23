import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка подключения (Render подхватит DATABASE_URL автоматически)
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
    number_plate = db.Column(db.String(20), unique=True)
    model = db.Column(db.String(50))
    capacity = db.Column(db.Integer)

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
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
    
    bus = db.relationship('Bus', backref='schedules')
    route = db.relationship('Route', backref='schedules')

# --- ЛОГИКА ПРИЛОЖЕНИЯ ---

@app.route('/')
def index():
    try:
        buses = Bus.query.all()
        drivers = Driver.query.all()
        routes = Route.query.all()
        # Сортируем расписание по времени
        schedules = Schedule.query.order_by(Schedule.departure_time).all()
        return render_template('index.html', buses=buses, drivers=drivers, routes=routes, schedules=schedules)
    except Exception as e:
        return f"Ошибка базы данных: {e}"

@app.route('/add_driver', methods=['POST'])
def add_driver():
    name = request.form.get('name')
    exp = request.form.get('exp')
    if name and exp:
        new_driver = Driver(full_name=name, experience=int(exp))
        db.session.add(new_driver)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    bus_id = request.form.get('bus_id')
    route_id = request.form.get('route_id')
    dep_time = request.form.get('dep_time')
    stop = request.form.get('stop')
    
    if bus_id and route_id and dep_time:
        new_sch = Schedule(
            bus_id=int(bus_id), 
            route_id=int(route_id), 
            departure_time=dep_time, 
            stop_name=stop
        )
        db.session.add(new_sch)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
