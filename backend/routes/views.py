from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

# Initialize the Blueprint for views
views_bp = Blueprint('views', __name__)

# ---------------------------
# Home Page Route
# ---------------------------
@views_bp.route('/')
def home_page():
    """
    Home Page Route
    Shows homepage for unauthenticated users or authenticated users.
    """
    try:
        if current_user.is_authenticated:
            return redirect(url_for('views.dashboard_page'))  # Redirect authenticated users to the dashboard
        return render_template('Homepage.html')  # Render homepage for non-authenticated users
    except Exception as e:
        # Log the error and show a user-friendly message
        print(f"Error on home_page route: {e}")
        return render_template('error.html', message="An unexpected error occurred.")

# ---------------------------
# Signup Page Route
# ---------------------------
@views_bp.route('/signup')
def signup_page():
    """
    Signup Page Route
    Renders the signup page only if the user is not authenticated.
    """
    try:
        if current_user.is_authenticated:
            return redirect(url_for('views.home_page'))  # Redirect to home page if user is already logged in
        return render_template('Signup.html')  # Render the signup page if not authenticated
    except Exception as e:
        print(f"Error on signup_page route: {e}")
        return render_template('error.html', message="An unexpected error occurred.")

# ---------------------------
# Login Page Route
# ---------------------------
@views_bp.route('/login')
def login_page():
    """
    Login Page Route
    Renders the login page only if the user is not authenticated.
    """
    try:
        if current_user.is_authenticated:
            return redirect(url_for('views.dashboard_page'))  # Redirect to dashboard if user is logged in
        return render_template('login.html')  # Render the login page for non-authenticated users
    except Exception as e:
        print(f"Error on login_page route: {e}")
        return render_template('error.html', message="An unexpected error occurred.")

# ---------------------------
# Dashboard Route (Requires Login)
# ---------------------------
@views_bp.route('/dashboard')
@login_required  # This route is protected, so login is required
def dashboard_page():
    """
    Dashboard Page Route
    Accessible only to authenticated users.
    """
    try:
        return f"Welcome to your dashboard, {current_user.username}!"  # Render simple dashboard message
        # Or use a template:
        # return render_template('dashboard.html')  # If you have a dashboard template
    except Exception as e:
        print(f"Error on dashboard_page route: {e}")
        return render_template('error.html', message="An unexpected error occurred.")

# ---------------------------
# Terms Page Route
# ---------------------------
@views_bp.route('/terms')
def terms_page():
    """
    Terms and Conditions Page Route
    """
    try:
        return render_template('terms.html')  # Render the terms page
    except Exception as e:
        print(f"Error on terms_page route: {e}")
        return render_template('error.html', message="An unexpected error occurred.")

# ---------------------------
# Privacy Page Route
# ---------------------------
@views_bp.route('/privacy')
def privacy_page():
    """
    Privacy Policy Page Route
    """
    try:
        return render_template('privacy.html')  # Render the privacy page
    except Exception as e:
        print(f"Error on privacy_page route: {e}")
        return render_template('error.html', message="An unexpected error occurred.")

