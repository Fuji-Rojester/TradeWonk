# backend/__init__.py

import os
from flask import Flask, jsonify # Removed unused template/redirect imports here
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
login_manager.login_view = 'auth.login' # Points to the login route in auth blueprint


# --- Application Factory Function ---
# Consider adding config_name='dev' and logic to load different configs
def create_app(config_class=Config):
    """Creates and configures the Flask application."""

    # Assumes templates/static folders are INSIDE backend/
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Initialize CORS - allowing credentials needed for Flask-Login sessions
    cors.init_app(app, supports_credentials=True)
    # In production, restrict origins:
    # origins = ["https://your-frontend-domain.com", "http://localhost:3000"] # Example
    # cors.init_app(app, origins=origins, supports_credentials=True)


    @login_manager.user_loader
    def load_user(user_id):
        # Import here to avoid circular imports
        from .models.user import User
        try:
            # Flask-Login passes user_id as string
            return User.query.get(int(user_id))
        except Exception as e:
            # Log error in production
            # app.logger.error(f"Error loading user {user_id}: {e}")
            return None

    # --- Import and Register Blueprints ---
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    try:
        from .routes.views import views_bp
        app.register_blueprint(views_bp, url_prefix='/') # Register page routes
    except ImportError:
        print("WARNING: Could not import or register views blueprint from routes.views.")
        pass

    # Add other blueprints here when created
    # from .routes.portfolio import portfolio_bp
    # app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')


    # --- Optional: Basic Error Handling ---
    @app.errorhandler(404)
    def not_found_error(error):
         # Could render a 404 template
         return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        # Important: Rollback session in case of DB error during request
        db.session.rollback()
        # Log error in production
        # app.logger.error(f'Server Error: {error}', exc_info=True)
        # Could render a 500 template
        return jsonify({'error': 'Internal Server Error'}), 500


    # --- Simple test route ---
    @app.route('/api/ping')
    def ping():
        return jsonify({"message": "Pong! TradeWonk API is running."})

    return app