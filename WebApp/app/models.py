from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash, secure_filename

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(256))  # Field to store the image path
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_img_path(self, path):
        self.image_path = secure_filename(path)
    
    def get_img_path(self, user_id):
        pass
        