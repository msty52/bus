class Schedule(db.Model):
    __tablename__ = 'Schedules'  
    id = db.Column('номер', db.Integer, primary_key=True)
    bus_id = db.Column('номер автобуса', db.Integer, db.ForeignKey('buses.id'))
    route_id = db.Column('идентификатор маршрута', db.Integer, db.ForeignKey('routes.id'))
    departure_time = db.Column('время отправления', db.Time)
    stop_name = db.Column('Название остановки', db.String)

    bus = db.relationship('Bus', backref='schedules')
    route = db.relationship('Route', backref='schedules')
