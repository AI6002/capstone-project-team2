from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from .models import User  # Import User from models.py

auth = Blueprint('auth', __name__)

# Your authentication routes go here:
# Login and logout routes here

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
