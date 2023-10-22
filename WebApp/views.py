from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import abort


# Define the blueprint
views = Blueprint('views', __name__)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role.name != 'Admin':
        abort(403)
    return render_template('admin_dashboard.html')

@views.route('/guest_dashboard')
def guest_dashboard():
    if current_user.is_authenticated and current_user.role.name != 'Guest':
        abort(403)
    return render_template('guest_dashboard.html')
