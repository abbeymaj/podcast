# Importing packages
import sys
import pandas as pd
import mlflow
import dagshub
import joblib
from src.components.config_entity import ModelURIConfig
from src.components.config_entity import DataTransformationConfig
from src.components.transform_data import TransformData
from src.utils import load_run_params
from src.utils import read_json_file
from src.exception import CustomException
from src.logger import logging

# Creating a class to make predictions
class MakePredictions():
    '''
    This class is responsible for making predictions on the data received from 
    the website.
    '''
    # Creating the constructor for the class
    def __init__(self):
        '''
        This is the constructor for the MakePredictions class.
        '''
        self.preprocessor_obj = DataTransformationConfig().preprocessor_obj_path
        self.model_uri = ModelURIConfig().model_uri
    
    # Creating a method to fetch the model params from the run_config folder
    def fetch_model_params(self):
        '''
        This method retrieves the model parameters for the latest trained model.
        ===================================================================================
        ----------------
        Returns:
        ----------------
        runs_data : json - This is the json file containing the model parameters for the 
        latest model.
        
        latest_model_uri : str - This is the uri for the latest model.
        ===================================================================================
        '''
        try:
            # Loading the run parameters
            run_params_json = load_run_params()
            
            # Reading the json file
            runs_data = read_json_file(run_params_json)
            
            # Fetching the model uri
            latest_model_uri = runs_data['model_uri']
            
            return runs_data, latest_model_uri
        
        except Exception as e:
            raise CustomException(e, sys)
    
    # Creating a method to fetch the latest model from the model registry
    def fetch_latest_model(self):
        '''
        This method retrieves the trained model from the model registry.
        ===================================================================================
        ----------------
        Returns:
        ----------------
        model : scikit-learn model - This is the trained model from the model registry.
        ===================================================================================
        '''
        try:
            # Initiating the dagshub client
            dagshub.init(repo_owner='abbeymaj', repo_name='podcast', mlflow=True)
            
            # Setting the model tracking URI
            mlflow.set_tracking_uri(self.model_uri)
            
            # Fetching the latest model uri
            _, latest_model_uri = self.fetch_model_params()
            
            # Fetch the model from the model registry
            model = mlflow.pyfunc.load_model(latest_model_uri)
            
            return model
        
        except Exception as e:
            raise CustomException(e, sys)
    
    # Creating a method to make predictions using the data entered by the user
    def make_predictions(self, features:pd.DataFrame):
        '''
        This method makes predictions using the feature inputs from the web page and 
        the trained model. This method also transforms the input data using the 
        preprocessor object before making the predictions.
        ============================================================================================
        -------------------
        Parameters:
        -------------------
        features : pandas dataframe - This is the feature data input received from the web page.
        
        -------------------
        Returns:
        -------------------
        preds : This is the prediction based on the input features.
        =============================================================================================
        '''
        try:
            logging.info("Making prediction on the input data from user.")
            
            # Fetching the preprocessor object
            preprocessor_obj = joblib.load(self.preprocessor_obj)
            
            # Fetch the trained model from the model registry
            model = self.fetch_latest_model()
            
            # Transforming the input features
            transform = TransformData()
            added_features = transform.generate_features(features)
            transformed_data = preprocessor_obj.transform(added_features)
            
            # Using the transformed feature set to make predictions
            preds = model.predict(transformed_data)
            preds = float(preds[0])
            
            logging.info("Prediction were made successfully!")
            
            return preds
            
        
        except Exception as e:
            raise CustomException(e, sys)