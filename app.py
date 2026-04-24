import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

uri = os.environ.get('DATABASE_URL')

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(20))
    model = db.Column(db.String(100))

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
    __tablename__ = 'Schedules'

    id = db.Column('номер', db.Integer, primary_key=True)
    bus_id = db.Column('номер автобуса', db.Integer, db.ForeignKey('buses.id'))
    route_id = db.Column('идентификатор маршрута', db.Integer, db.ForeignKey('routes.id'))
    departure_time = db.Column('время отправления', db.Time)
    stop_name = db.Column('Название остановки', db.String(100))
    
    bus = db.relationship('Bus', backref='schedules')
    route = db.relationship('Route', backref='schedules')

@app.route('/')
def index():
    try:
        # Загружаем данные для табло
        drivers = Driver.query.all()
        schedules = Schedule.query.order_by(Schedule.departure_time).all()
        return render_template('index.html', drivers=drivers, schedules=schedules)
    except Exception as e:
        return f"Ошибка базы данных: {e}"

if __name__ == '__main__':
    app.run(debug=True)
