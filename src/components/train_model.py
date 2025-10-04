# Importing packages
import sys
import numpy as np
import pandas as pd
import joblib
import sklearn
sklearn.set_config(transform_output='pandas')
from sklearn.linear_model import BayesianRidge
from sklearn.metrics import mean_squared_error
from src.components.config_entity import ModelTrainerConfig
from src.components.config_entity import CreateFeatureStoreConfig
from src.components.find_best_model import FindBestModel
from src.exception import CustomException
from src.logger import logging

# Creating a class to train the model
class TrainModel():
    '''
    This class is used to train the model. The class has three methods - 
    the constructor, a method to split the datasets into features & targets,
    and a method to initiate the model training.
    '''
    # Creating the constructor for the model trainer class
    def __init__(self):
        '''
        This is the constructor for the model training class. The constructor
        initializes the path to the transformed datasets and also initializes the 
        path to which the trained model will be stored (if needed).
        '''
        self.feature_store_config = CreateFeatureStoreConfig()
        self.trained_model_config = ModelTrainerConfig()
    
    # Creating a method to split the datasets into feature and target datasets
    def create_feature_target_sets(self):
        '''
        This method creates the feature and target datasets.
        ============================================================================       
        -------------------
        Returns:
        -------------------
        X_train : pandas dataframe - The training feature set.
        y_train : pandas dataframe - The training target set.
        X_test : pandas dataframe - The test feature set.
        y_test : pandas dataframe - The test target set.
        =============================================================================
        '''
        try:
            logging.info("Creating the feature and target datasets.")
            
            # Reading the transformed train and test datasets
            train_data = pd.read_parquet(self.feature_store_config.xform_train_data)
            test_data = pd.read_parquet(self.feature_store_config.xform_test_data)
            
            # Splitting the train dataset into a feature and target dataset
            X_train = train_data.copy().drop(labels=['Listening_Time_minutes'], axis=1)
            y_train = train_data['Listening_Time_minutes'].copy()
            
            # Splitting the test dataset into a feature and target datasets
            X_test = test_data.copy().drop(labels=['Listening_Time_minutes'], axis=1)
            y_test = test_data['Listening_Time_minutes']
            
            logging.info('Successfully created the feature and target datasets.')
            
            return (
                X_train, 
                X_test, 
                y_train,
                y_test 
            )
        
        except Exception as e:
            raise CustomException(e, sys)
    
    # Creating a method to initiate the model training process.
    def initiate_model_training(self, save_model=False, make_prediction=False):
        '''
        This method trains the model and then saves the trained model to the artifacts
        folder.
        ===================================================================================
        ------------------------
        Parameters:
        ------------------------
        save_model : bool - This determines if the model should be saved in the artifacts
        folder. The default value is False.
        
        make_prediction : bool - This determines if the model should make a prediction, 
        calculate the metric and return the metric. This will be used for testing purposes.
        The default value is False.
        
        ------------------------
        Returns:
        ------------------------
        model_path : str - This is the path to the saved model.
        best_params : dict - This is the best hyperparameters for the best model.
        metric : float - This is the metric from the prediction. This will be returned
        if the user sets the make_prediction flag to True. 
        ====================================================================================
        '''
        try:
            logging.info('Initiating the model training process.')
            
            # Fetching the feature and target datasets
            X_train, X_test, y_train, y_test = self.create_feature_target_sets()
            
            # Instantiating the linear regression model
            lr_model = BayesianRidge()
            
            # Defining the parameters to search for the best model
            params = {
                'max_iter': [300, 400, 500],
                'tol': [0.01, 0.001, 0.0001],
                'alpha_1': [1e-04, 1e-05, 1e-06],
                'alpha_2': [1e-04, 1e-05, 1e-06],
                'lambda_1': [1e-04, 1e-05, 1e-06],
                'lambda_2': [1e-04, 1e-05, 1e-06]
            }
            
            # Finding the best model
            bst_model = FindBestModel()
            best_model, best_params = bst_model.find_best_model(
                estimator=lr_model,
                params=params,
                train_set=X_train,
                target_set=y_train,
                cv=3
            )
            
            logging.info('Model training process completed.')
            
            # Saving the model if save_model flag is set to True
            if save_model:
                joblib.dump(best_model, self.trained_model_config.model_path)
            
            # Making a prediction when the make_prediction flag is set to True
            if make_prediction:
                y_pred = best_model.predict(X_test)
                metric = np.sqrt(mean_squared_error(y_test, y_pred))
                
                return (
                    best_model,
                    best_params,
                    metric
                )
            
            else:
                return (
                    best_model,
                    best_params
                )
                
        
        except Exception as e:
            raise CustomException(e, sys)
        