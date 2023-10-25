import flask_sqlalchemy

from . import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    goal_date = db.Column(db.Date)
    completed = db.Column(db.Boolean)
