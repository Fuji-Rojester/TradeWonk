# backend/routes/auth.py

# Import the 're' module for regular expressions at the top
import re
from flask import Blueprint, jsonify, request
from .. import db
from ..models.user import User
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

# ---------------------------
# 🔒 Validation Helpers
# ---------------------------
def is_valid_username(username):
    return username and len(username) >= 3

def is_strong_password(password):
    if not password or len(password) < 9:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    return has_upper and has_lower and has_symbol

# --- NEW Email Format Validation Helper ---
def is_valid_email_format(email):
    if not email:
        return False
    # Basic regex for something@something.something structure
    # Allows letters, numbers, ., _, %, +, - before @
    # Allows letters, numbers, ., - after @
    # Requires a dot . and at least two letters for the domain ending (e.g., .com, .io)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
# --- END NEW Helper ---

# ---------------------------
# 🔐 Registration Route
# ---------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Validation
    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    if not is_valid_username(username):
        return jsonify({'error': 'Username must be at least 3 characters'}), 400

    # --- Use the new email format check ---
    if not is_valid_email_format(email):
         return jsonify({'error': 'Invalid email format'}), 400
    # --- End email format check ---

    if not is_strong_password(password):
        return jsonify({
            'error': 'Password must be at least 9 characters, with uppercase, lowercase, and a symbol'
        }), 400

    # Check uniqueness
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Create user
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # Optional auto-login
    # login_user(new_user)

    return jsonify({'message': 'User registered successfully'}), 201

# --- (rest of your code: /login, /logout, /status, /check-username remains the same) ---

# ---------------------------
# ✅ Login Route
# ---------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    email_or_username = data.get('email') or data.get('username')
    password = data.get('password')
    remember = data.get('remember', False) # Default remember to False

    if not email_or_username or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter(
        (User.email == email_or_username) | (User.username == email_or_username)
    ).first()

    if user and user.check_password(password):
        login_user(user, remember=remember)
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401

# ---------------------------
# 🚪 Logout Route
# ---------------------------
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# ---------------------------
# 👤 Status Route
# ---------------------------
@auth_bp.route('/status')
@login_required
def status():
    return jsonify({
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email
        }
    }), 200

# ---------------------------
# 🔍 Check Username Availability
# ---------------------------
@auth_bp.route('/check-username', methods=['POST'])
def check_username():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "Username not provided"}), 400

    username = data['username'].strip()

    if not is_valid_username(username):
        # You might return an error instead if the username is too short based on policy
        return jsonify({"exists": False, "message": "Username format invalid (too short)"}), 200 # Or 400?

    user = User.query.filter_by(username=username).first()

    return jsonify({"exists": bool(user)}), 200