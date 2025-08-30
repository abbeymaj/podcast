# Importing packages
import sys
import os
import pandas as pd
from src.components.config_entity import CreateFeatureStoreConfig
from src.logger import logging
from src.exception import CustomException

# Creating a class to create the feature store and store the transformed datasets
class CreateFeatureStore():
    '''
    This class contains methods to create the feature store and then store the transformed datasets. 
    The class contains two methods - a constructor and a method to store the transformed
    datasets.
    '''
    # Creating the constructor for the class
    def __init__(self):
        '''
        This is the constructor for the create feature store class.
        '''
        self.feature_store_config = CreateFeatureStoreConfig()
    
    # Creating a method to store the transformed datasets
    def create_and_store_features(self, train_data:pd.DataFrame, test_data:pd.DataFrame):
        '''
        This method stores the transformed datasets in the feature store folder.
        ==========================================================================
        ----------------
        Parameters:
        ----------------
        train_path : pandas dataframe - This is the train dataset.
        test_path : pandas dataframe - This is the test dataset.
        
        ----------------
        Returns:
        ----------------
        transformed train data path : str - Returns the path to the transformed train dataset.
        transformed test data path : str - Returns the path to the transformed test dataset.
        ===========================================================================
        '''
        try:
            logging.info("Beginning the creation of the feature store.")
            
            # Creating the feature store folder
            dir_name = os.path.dirname(self.feature_store_config.xform_train_data)
            os.makedirs(dir_name, exist_ok=True)
            
            # Storing the transformed datasets in the feature store
            train_data.to_parquet(self.feature_store_config.xform_train_data, index=False, compression='gzip')
            test_data.to_parquet(self.feature_store_config.xform_test_data, index=False, compression='gzip')
            
            logging.info("Feature store created successfully.")
            
            return (
                self.feature_store_config.xform_train_data,
                self.feature_store_config.xform_test_data
            )
        
        except Exception as e:
            raise CustomException(e, sys)



