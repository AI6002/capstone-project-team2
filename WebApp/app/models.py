from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

def hash_password(password):
    # Convert the password to bytes, if it's not already in bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password

def check_password(stored_password, provided_password):
    # Convert the provided password to bytes
    provided_password_bytes = provided_password.encode('utf-8')

    # Check if the provided password matches the stored hashed password
    return bcrypt.checkpw(provided_password_bytes, stored_password)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(256))  # Field to store the image path
    
    def set_password(self, password):
        # self.password = generate_password_hash(password, method='sha256')
        self.password = hash_password(password)
        
    def check_password(self, password):
        return check_password(self.password, password)
        # return check_password_hash(self.password, password)
    
    def set_img_path(self, path):
        self.image_path = path
        