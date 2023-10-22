from flask import render_template, request
from flask_login import LoginManager
from web import create_app, db
from web.models import User, Role
from web.auth import auth
from web.views import views  # Importing views blueprint
import os

app = create_app()  # creating an instance of your application

app.secret_key = os.environ.get('SECRET_KEY', 'Team2')  # Using a fallback value if the environment variable is not found

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(views)  # Register the views blueprint here

@login_manager.user_loader
def load_user(user_id):  # Callback to reload the user object
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        image = request.files['image']
        question = request.form['question']
        answer = "This is a dummy answer for the question: " + question
    return render_template('home.html', answer=answer)  # Using home.html from templates folder

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error=str(e)), 500

def insert_roles():
    roles = ['Guest', 'User', 'Admin']
    for role in roles:
        existing_role = Role.query.filter_by(name=role).first()
        if not existing_role:
            role_to_insert = Role(name=role)
            db.session.add(role_to_insert)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created here first
        insert_roles()  # Then insert roles
    app.run(debug=True)

