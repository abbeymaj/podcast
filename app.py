# Importing packages
import pandas as pd
from flask import Flask, request, render_template, jsonify
from src.components.create_custom_data import CreateCustomData
from src.components.make_predictions import MakePredictions 

# Creating the flask app
app = Flask(__name__)

# Creating the home page
@app.route('/')
def index():
    '''
    This function creates the home page for the application.
    '''
    return render_template('index.html')