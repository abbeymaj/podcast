# Importing packages
import pandas as pd
from flask import Flask, request, render_template, jsonify
from src.components.create_custom_data import CreateCustomData
from src.components.make_predictions import MakePredictions 

# Creating the flask app
app = Flask(__name__)

# Creating the home page
@app.route('/')
@app.route('/home')
def index():
    '''
    This function creates the home page for the application.
    '''
    return render_template('index.html')

# Creating a function to make predictions using user entered data
@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    '''
    This function will display the prediction landing page if the method is "GET".
    If the method is "POST", the function will run the prediction.
    '''
    # Retrieving the prediction page if the method is "GET"
    if request.method == "GET":
        return render_template('predict.html')
    
    # If the method is "POST", then run the prediction
    elif request.method == "POST":
        # Capturing the data entered by the user
        data = CreateCustomData(
            Podcast_Name = str(request.form.get('Podcast_Name')),
            Episode_Length_minutes = float(request.form.get('Episode_Length_minutes')),
            Genre = str(request.form.get('Genre')),
            Publication_Day = str(request.form.get('Publication_Day')),
            Publication_Time = str(request.form.get('Publication_Time'))
        )
        
        # Creating a dataframe from the user entered data
        df = data.create_dataframe()
        df.drop(labels=['time'], axis=1, inplace=True)
        
        # Making predictions using the user entered data
        prediction = MakePredictions()
        preds = prediction.make_predictions(df)
        
        # Returning the prediction to the web application
        return render_template('predict.html', results=preds, pred_df=df)

# Running the Flask app
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Failed to run the Flask app: {e}")