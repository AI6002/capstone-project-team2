from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(256))  # Field to store the image path
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_img_path(self, path):
        self.image_path = path

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(db.Integer, nullable=False)
    reaction_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'

    # Define a relationship with the User model
    user = db.relationship('User', backref=db.backref('reactions', lazy=True))
        