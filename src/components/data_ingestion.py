# Importing packages
import os
import sys
import pandas as pd
from sklearn import set_config
set_config(transform_output='pandas')
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging
from src.components.config_entity import DataIngestionConfig

# Creating a class to ingest the data
class DataIngestion():
    '''
    This class is used to ingest the raw data and split the dataset into a
    train and test dataset. Both the train and test dataset are then stored
    in the artifacts folder.
    '''
    # Creating the constructor for the data ingestion class
    def __init__(self):
        '''
        This is the constructor for the data ingestion class.
        '''
        self.ingestion_config = DataIngestionConfig()
    
    # Creating a method to initiate the data ingestion process
    def initiate_data_ingestion(self):
        '''
        This method will ingest the data from source, split the dataset into a train
        and test dataset. The function will also create the artifacts folder and store
        the train and test dataset in the artifacts folder.
        ====================================================================================
        ---------------
        Returns:
        ---------------
        train file path : str - This is the path to the train dataset.
        test file path : str - This is the path to the test dataset.
        ====================================================================================
        '''
        try:
            # Creating the artifacts folder if the folder does not exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            # Defining the path to the raw data
            raw_data_path = self.ingestion_config.raw_data_path
            
            # Reading the raw data from the source
            df = pd.read_parquet(raw_data_path)
            
            # Dropping features that will not be used
            cols_to_drop = [
                'id',
                'Episode_Title',
                'Host_Popularity_percentage',
                'Guest_Popularity_percentage',
                'Number_of_Ads',
                'Episode_Sentiment'
            ]
            df.drop(labels=cols_to_drop, axis=1, inplace=True)
            
            # Splitting the dataset into a train and test dataset
            train_data, test_data = train_test_split(df, test_size=0.3, random_state=42)
            
            # Storing the train and test datasets in the artifacts folder
            train_data.to_parquet(self.ingestion_config.train_data_path, index=False, compression='gzip')
            test_data.to_parquet(self.ingestion_config.test_data_path, index=False, compression='gzip')
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e, sys)