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

    # Creating an app instance in Flask with correct template and static folders
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Configure SQLAlchemy with absolute URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///podcast.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Registering the models
    db.init_app(app)

    return app