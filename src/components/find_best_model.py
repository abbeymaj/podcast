# Importing packages
import sys
import pandas as pd
import sklearn
sklearn.set_config(transform_output='pandas')
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from src.components.config_entity import ModelTrainerConfig
from src.exception import CustomException
from src.logger import logging 


# Creating a class to find the best model, given a set of parameters.
class FindBestModel():
    '''
    This class is used to find the best model, given a set of parameters. The
    class has one method (other than the constructor) - find_best_model. 
    '''
    # Creating the constructor for the class
    def __init__(self):
        '''
        This is the constructor for the FindBestModel class. The constructor
        initializes the path to which the model will be stored.
        '''
        self.model_trainer_config = ModelTrainerConfig()
    
    # Creating a method to find the best model
    def find_best_model(
        self,
        estimator,
        params:dict,
        train_set:pd.DataFrame,
        target_set:pd.DataFrame,
        cv:int=5
        ):
        '''
        This method is used to find the best model, given the hyperparameters.
        =================================================================================
        ----------------
        Parameters:
        ----------------
        params : dict - This is the dictionary containing the hyperparameters for the model.
        train_set : pandas dataframe - This is the training dataset.
        target_set : pandas dataframe - This is the target dataset.
        cv : int - This is the number of cross-validation folds.
        
        ----------------
        Returns:
        ----------------
        best_model : scikit-learn model - This is the best model found.
        best_params : dict - This is the dictionary containing the best parameters.
        =================================================================================
        
        '''
        try:
            logging.info('Starting the search for the best model.')
            
            # Instantiating a Grid Search CV object
            grid_search = HalvingGridSearchCV(
                estimator=estimator,
                param_grid=params,
                cv=cv,
                scoring='neg_mean_squared_error',
                refit=True,
                verbose=3,
                n_jobs=-1
            )
            
            # Fitting the grid search object to the training data
            grid_search.fit(train_set, target_set)
            
            # Extracting the best model and best parameters
            best_model = grid_search.best_estimator_
            best_params = grid_search.best_params_
            
            logging.info('Best model found.')
            
            return (
                best_model, 
                best_params
                )
        
        except Exception as e:
            raise CustomException(e, sys)