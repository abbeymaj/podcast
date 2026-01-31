# Importing packages
from src.web_components.create_app import create_app
from src.web_components.routes import main_bp

# Creating the Flask app
app = create_app()

# Registering the routers
app.register_blueprint(main_bp)

# Running the Flask app
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Failed to run the Flask app: {e}")