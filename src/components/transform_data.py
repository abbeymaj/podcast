# Importing packages
import sys
import pandas as pd
import joblib
import sklearn
sklearn.set_config(transform_output='pandas')
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from feature_engine.encoding import DecisionTreeEncoder
from src.components.config_entity import DataTransformationConfig
from src.exception import CustomException
from src.logger import logging

# Creating a class to create features and transform the datasets
class TransformData():
    '''
    This class transforms the raw data and prepares the data for storage in the
    feature store. The class has three methods - The constructor, a method to create
    features, a method to create the preprocessor object and a method to 
    initiate the data transformation process. 
    '''
    # Creating the constructor for the transform data class
    def __init__(self):
        '''
        This is the constructor for the transform data class. This
        constructor does not have any parameters.
        '''
        preprocessor_obj_config = DataTransformationConfig()
    
    # Creating a method to generate features
    def generate_features(self, df:pd.DataFrame)->pd.DataFrame:
        '''
        This method accepts a pandas dataframe, generates features and returns
        a pandas dataframe with the new features.
        ==================================================================================
        ---------------
        Parameters:
        ---------------
        df : Pandas Dataframe - This is the dataframe with the raw data.
        
        ---------------
        Returns:
        ---------------
        df : Pandas Dataframe - This is the dataframe with the new features. 
        ==================================================================================
        '''
        try:
            logging.info('Concatenating the publication date and time features.')
            
            # Concatenating the publication date and time features
            df['Pub_Day_Time'] = df['Publication_Day'] + '_' + df['Publication_Time']
            
            # Dropping the publication date and time features
            df.drop(labels=['Publication_Day', 'Publication_Time'], axis=1, inplace=True)
            
            logging.info('Sucessfully concatenated the publication date and time features')
            
            return df
        
        except Exception as e:
            raise CustomException(e, sys)
    
    # Creating a method to construct the preprocessor object
    def create_preprocessor_obj(self):
        '''
        This method constructs the preprocessor object, using scikit-learn's 
        ColumnTransformer pipeline and returns the created preprocessor object.
        ==================================================================================
        ---------------
        Returns:
        ---------------
        preprocessor_obj : scikit-learn ColumnTransformer pipeline - This is the 
        preprocessor object to transform the data.
        ==================================================================================
        '''
        try:
            logging.info('Creating the preprocessor object.')
            
            # Defining the numerical columns 
            num_cols = ['Episode_Length_minutes']
            
            # Defining the categorical columns
            cat_cols = [x for x in list(df.columns) if x not in num_cols]
            
            # Creating the numeric pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('impute', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )
            
            # Creating the categorical pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('tree_encoder', DecisionTreeEncoder(
                        cv=3, 
                        scoring='roc_auc', 
                        precision=3, 
                        random_state=42
                        )
                     ),
                    ('std_scaler', StandardScaler())
                ]
            )
            
            # Creating the final pipeline
            preprocessor_obj = ColumnTransformer(
                transformers=[
                    ('num_pipeline', num_pipeline, num_cols),
                    ('cat_pipeline', cat_pipeline, cat_cols)
                ]
            )
            
            logging.info('Preprocessor object created successfully.')
            
            return preprocessor_obj
        
        except Exception as e:
            raise CustomException(e, sys)
    
    # Creating a method to initiate the data transformation process.
    def initiate_data_transformation(self, train_path:str, test_path:str):
        '''
        This method initiates the data transformation process. The method accepts the
        train data path and the test data path, transforms the data and returns the 
        transformed data as well as the preprocessor object.
        ===================================================================================
        ---------------
        Parameters:
        ---------------
        train_path : str - This is the path to the train dataset.
        test_path : str - This is the path to the test dataset.
        
        ---------------
        Returns:
        ---------------
        train_arr : Pandas Dataframe - This is the transformed train dataset.
        test_arr : Pandas Dataframe - This is the transformed test dataset.
        preprocessor_obj : scikit-learn ColumnTransformer pipeline - This is the 
        preprocessor object to transform the data.
        ====================================================================================
        '''
        try:
            pass
        
        except Exception as e:
            raise CustomException(e, sys)