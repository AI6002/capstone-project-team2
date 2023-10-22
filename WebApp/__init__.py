from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # initialize without app context

def create_app():
    app = Flask(__name__, template_folder='/Users/mba/Desktop/myworkspace/Flask_VQA/templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)  # associate db instance with app context
    
    return app



