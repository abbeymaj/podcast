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
from src.components.config_entity import DataIngestionConfig
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
        self.data_ingestion_config = DataIngestionConfig()
        self.preprocessor_obj_config = DataTransformationConfig()
    
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
    def create_preprocessor_obj(self, df:pd.DataFrame):
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
    def initiate_data_transformation(self, train_path:str, test_path:str, save_object=True):
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
            logging.info('Initiating the data transformation process.')
            
            # Reading the train and test datasets
            train_data = pd.read_parquet(self.data_ingestion_config.train_data_path)
            test_data = pd.read_parquet(self.data_ingestion_config.test_data_path)
            
            # Separating the train data into feature and target sets
            train_features = train_data.copy().drop(labels=['Listening_Time_minutes'], axis=1)
            train_target = train_data['Listening_Time_minutes'].copy()
            
            # Separating the test data into feature and target sets
            test_features = test_data.copy().drop(labels=['Listening_Time_minutes'], axis=1)
            test_target = test_data['Listening_Time_minutes'].copy()
            
            # Generating features for the train and test datasets
            train_df = self.generate_features(train_features)
            test_df = self.generate_features(test_features)
            
            # Creating the preprocessor object
            preprocessor_obj = self.create_preprocessor_obj(train_df)
            
            # Transforming the train and test features
            train_arr = preprocessor_obj.fit_transform(train_df, train_target)
            test_arr = preprocessor_obj.transform(test_df)
            
            # Concatenating the train and test features and targets to store in the feature store
            train_data_combined = pd.concat([train_arr, train_target], axis=1)
            test_data_combined = pd.concat([test_arr, test_target], axis=1)
            
            # Saving the preprocessor object if the save_object flag is set to True
            if save_object:
                joblib.dump(preprocessor_obj, self.preprocessor_obj_config.preprocessor_obj_path)
            
            logging.info('Data transformation process completed sucessfully.')
            
            return (
                train_data_combined,
                test_data_combined,
                preprocessor_obj
            )
        
        except Exception as e:
            raise CustomException(e, sys)