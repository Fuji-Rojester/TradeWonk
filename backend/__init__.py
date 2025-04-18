# backend/__init__.py

import os
# Added render_template, redirect, url_for for the views blueprint
from flask import Flask, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager

# Import the configuration class relatively
from .config import Config

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
login_manager = LoginManager()
# Point to the login route within the 'auth' blueprint
login_manager.login_view = 'auth.login'
# Optional: customize message for login_required
# login_manager.login_message = "Please log in to access this page."
# login_manager.login_message_category = "info"


# --- Application Factory Function ---
def create_app(config_class=Config):
    """Creates and configures the Flask application."""

    app = Flask(__name__,
                # Optional: Specify template/static folders relative to 'backend'
                # if your HTML/CSS/JS are *not* inside backend/templates and backend/static
                # template_folder='templates',
                # static_folder='static'
               )
    app.config.from_object(config_class)

    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # Allow requests from localhost:3000 (React default) for API routes
    # You might need different CORS config if Flask serves HTML too
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


    # User Loader function required by Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Import User model here to avoid potential circular imports during init
        from .models.user import User
        try:
            # Ensure user_id is integer before querying
            user = User.query.get(int(user_id))
            return user
        except Exception as e:
            # Optional: Log the exception
            # app.logger.error(f"Error loading user {user_id}: {e}")
            return None

    # --- Import and Register Blueprints ---
    # Import blueprints inside the factory
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # --- ADDED VIEW BLUEPRINT REGISTRATION ---
    # Make sure you have created backend/routes/views.py with views_bp defined
    try:
        from .routes.views import views_bp
        app.register_blueprint(views_bp) # Register routes like /signup, /login pages etc.
    except ImportError:
        # Handle case where views.py might not exist yet gracefully
        print("WARNING: Could not import or register views blueprint from routes.views.")
        pass


    # --- Placeholder Registrations (Uncomment when ready) ---
    # from .routes.portfolio import portfolio_bp
    # app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')

    # from .routes.import_data import import_bp
    # app.register_blueprint(import_bp, url_prefix='/api/import')

    # --- Define a simple test route ---
    @app.route('/api/ping')
    def ping():
        return jsonify({"message": "Pong! TradeWonk API is running."})

    return app