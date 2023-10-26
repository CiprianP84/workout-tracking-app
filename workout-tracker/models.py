from . import db    # we import our db
from flask_login import UserMixin  # we need to mix user with login manager
from datetime import datetime
from sqlalchemy.sql import func


class User(db.Model, UserMixin):    # we define the user model that will inherit from db.model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    workouts = db.relationship('Workout', backref='author', lazy=True)

# class Workout(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     exercise = db.Column(db.Text, nullable=False)
#     weight = db.Column(db.Integer, default='-', nullable=True)
#     sets = db.Column(db.Integer, nullable=False)
#     reps = db.Column(db.Integer, nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
#     comment = db.Column(db.Text, default='No comment', nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Integer, default=0, nullable=True)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=func.now())  # Use func.now() for the default timestamp
    comment = db.Column(db.Text, default='No comment', nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)