from flask import Flask
from extensions import db, login_manager
from models import User

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'team2vqa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vqa_users.db'  # SQLite database file

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
