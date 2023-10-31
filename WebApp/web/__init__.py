from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # initialize without app context

def create_app(template_dir, static_dir):
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)  # associate db instance with app context
    
    return app



