# Importing packages
import pandas as pd
from flask import Flask, request, render_template, jsonify
from src.components.create_app import create_app, db
from src.components.models import Data, Predictions
from src.components.create_custom_data import CreateCustomData
from src.components.make_predictions import MakePredictions 

# Creating the flask app
app = create_app()

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
        
        # Loading the data into the database
        user_data = Data(
            Podcast_Name = str(request.form.get('Podcast_Name')),
            Episode_Length_minutes = float(request.form.get('Episode_Length_minutes')),
            Genre = str(request.form.get('Genre')),
            Publication_Day = str(request.form.get('Publication_Day')),
            Publication_Time = str(request.form.get('Publication_Time'))
        )
        db.session.add(user_data)
        db.session.flush()
        
        # Creating a dataframe from the user entered data
        df = data.create_dataframe()
        df.drop(labels=['time'], axis=1, inplace=True)
        
        # Making predictions using the user entered data
        prediction = MakePredictions()
        preds = prediction.make_predictions(df)
        
        # Storing the predictions in the database
        preds_data = Predictions(
            data_id = user_data.id,
            prediction = preds
        )
        db.session.add(preds_data)
        db.session.commit()
        
        # Returning the prediction to the web application
        return render_template('predict.html', results=preds, pred_df=df)

# Running the Flask app
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Failed to run the Flask app: {e}")