import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Creating the database instance
db = SQLAlchemy()

# Creating the app function
def create_app():

    # Get the root directory (where app.py is located)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    template_dir = os.path.join(root_dir, 'templates')
    static_dir = os.path.join(root_dir, 'static')
    db_dir = os.path.join(root_dir, 'db')

    # Create db directory if it doesn't exist
    os.makedirs(db_dir, exist_ok=True)

    # Creating an app instance in Flask with correct template and static folders
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Configure SQLAlchemy with absolute URI pointing to db folder
    db_path = os.path.join(db_dir, 'podcast.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Registering the models
    db.init_app(app)

    return app