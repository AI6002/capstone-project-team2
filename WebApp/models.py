#from . import db  # Import db from __init__.py
from datetime import datetime
from web import db
from flask_login import UserMixin

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Role('{self.name}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=2)  # default to User role

    role = db.relationship('Role')  # New relationship to the Role model

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False)
    question_text = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Reference to user

    def __repr__(self):
        return f"Question('{self.image_file}', '{self.question_text}', '{self.date_posted}')"
