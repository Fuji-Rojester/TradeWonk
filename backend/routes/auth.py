# backend/routes/auth.py
import re
from flask import Blueprint, jsonify, request
from .. import db
from ..models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timezone # Ensure timezone is imported

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

def is_valid_email_format(email):
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ---------------------------
# 🔐 Registration Route
# ---------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    # Normalize before validation/checks
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower() # Lowercase email immediately
    password = data.get('password', '')

    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    if not is_valid_username(username):
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    if not is_valid_email_format(email):
         return jsonify({'error': 'Invalid email format'}), 400
    if not is_strong_password(password):
        return jsonify({
            'error': 'Password must be at least 9 characters, with uppercase, lowercase, and a symbol'
        }), 400

    # Use normalized values for checks
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Use normalized values for creation
    new_user = User(username=username, email=email)
    new_user.set_password(password) # Hashes the password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# ---------------------------
# ✅ Login Route
# ---------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    # Get identifier (could be email or username) and password
    email_or_username = data.get('email') or data.get('username')
    password = data.get('password')
    remember = data.get('remember', False) # Get remember status

    if not email_or_username or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    # Prepare identifier for query (lowercase if it's an email)
    login_identifier = email_or_username.strip()
    is_email = '@' in login_identifier
    if is_email:
        login_identifier_for_query = login_identifier.lower()
    else:
        login_identifier_for_query = login_identifier

    # Find user by email (case-insensitive) or username (case-sensitive, adjust if needed)
    if is_email:
        user = User.query.filter(User.email == login_identifier_for_query).first()
    else:
        user = User.query.filter(User.username == login_identifier_for_query).first()


    if user and user.check_password(password):
        login_user(user, remember=remember) # Pass remember status

        # Track last login time
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()

        # Return user data using the model's method
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200

    # If authentication failed
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
    # Return current user data using the model's method
    return jsonify({'user': current_user.to_dict()}), 200

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
        # Consistent error format might be better
        return jsonify({"error": "Username format invalid (too short)"}), 400

    user = User.query.filter_by(username=username).first()
    # Return boolean directly in the expected format
    return jsonify({"exists": bool(user)}), 200