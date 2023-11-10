from flask import render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .extensions import db
from .models import User

def init_routes(app):
    # Handle Landing Page
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return redirect(url_for('login'))

    # Authenticated home view
    @app.route('/home')
    @login_required
    def home():
        username = current_user.username
        return render_template('home.html', username=username)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            try:
                # Extract Username and Email
                username = request.form['username']
                email = request.form['email']
                
                # Extract password and hash it
                password = request.form['password']
                hashed_password = generate_password_hash(password, method='sha256')

                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                
                return redirect(url_for('login'))
            
            except Exception as e:
                # If there is any error, flash a message to the user
                flash(str(e))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            # Extract the username and password from form data
            username = request.form['username']
            password = request.form['password']

            # Use username to find user 
            user = User.query.filter_by(username=username).first()
            if user:
                # Validate password
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('home'))

            flash('Invalid username or password')
        return render_template('login.html')


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # Error handler
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error=str(e)), 500

    # Command to create the database tables
    @app.cli.command('create-db')
    def create_db():
        """Create the database."""
        db.create_all()
        print("Database Tables created.")
