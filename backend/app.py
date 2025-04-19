# app.py (Located in the main TradeWonk directory)

from backend import create_app

# Create the Flask app instance using the factory
# Ensure create_app loads the appropriate config (Dev/Prod)
app = create_app() # You might pass 'dev' or 'prod' based on environment

if __name__ == "__main__":
    # Consider using environment variables for host/port/debug in production scenarios
    # Example: host=os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    # Example: port=int(os.getenv('FLASK_RUN_PORT', 5000))
    # Example: debug=os.getenv('FLASK_DEBUG', '1') == '1'
    app.run(debug=True) # debug=True is okay for local dev, ensure False in prod config