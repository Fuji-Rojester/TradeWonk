# backend/routes/views.py
from flask import Blueprint, render_template
from flask_login import current_user # Optional: to redirect if already logged in

views_bp = Blueprint('views', __name__)

@views_bp.route('/signup')
def signup_page():
    # Optional: If user is already logged in, redirect them away
    # if current_user.is_authenticated:
    #     return redirect(url_for('views.dashboard_page')) # Assuming you have a dashboard route later
    return render_template('Signup.html')

# Add routes for login page, homepage etc. here later
# @views_bp.route('/login')
# def login_page():
#     return render_template('login.html')

# @views_bp.route('/')
# def home_page():
#     return render_template('Homepage.html')