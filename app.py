import os
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Твоя строка подключения (не забудь пароль!)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ТВОЙ_ПАРОЛЬ@db.kzgtonlqmkcvlhcshmgp.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Описание таблицы автобусов
class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(20))
    model = db.Column(db.String(50))
    capacity = db.Column(db.Integer)

# Главная страница
@app.route('/')
def index():
    try:
        all_buses = Bus.query.all()
        # Простой HTML прямо в коде для теста
        html = """
        <h1>Список автобусов в парке</h1>
        <table border="1">
            <tr>
                <th>Номер</th>
                <th>Модель</th>
                <th>Вместимость</th>
            </tr>
            {% for bus in buses %}
            <tr>
                <td>{{ bus.number_plate }}</td>
                <td>{{ bus.model }}</td>
                <td>{{ bus.capacity }}</td>
            </tr>
            {% endfor %}
        </table>
        """
        return render_template_string(html, buses=all_buses)
    except Exception as e:
        return f"Ошибка: {e}"

if __name__ == '__main__':
    app.run(debug=True)