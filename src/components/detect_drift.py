import sys
import os
import pandas as pd 
from evidently import Dataset, DataDefinition, Report, Regression
from evidently.presets import DataDriftPreset
from src.components.config_entity import DataIngestionConfig
from src.components.config_entity import DriftDetectorConfig
from src.utils import read_sql_data
from src.exception import CustomException

# Creating a class to detect data drift within the feature and targets
class DetectDataDrift():
    '''
    This class is used to detect data drifts in the features and target.
    '''
    # Creating the constructor for the class
    def __init__(self):
        '''
        This is the constructor for the DetectDrift class.
        '''
        self.report_config = DriftDetectorConfig()
        self.ingestion_config = DataIngestionConfig()

    # Creating a method to read the data from the database
    def read_data_from_db(self):
        '''
        This method reads the data from both tables in the database, merges the tables
        and the returns the merged dataset.
        '''
        try:
            # Reading the data from the "data" table
            data_df = read_sql_data(table='data')
            
            # Reading the data from the "predictions" table
            preds_df = read_sql_data(table='predictions')
            
            # Merging both data dataframes
            merged_df = data_df.merge(preds_df, left_on='id', right_on='data_id', how='left')
            
            # Defining which features to keep (other than the target feature)
            cols_to_keep = [
                'Podcast_Name',
                'Episode_Length_minutes',
                'Genre',
                'Publication_Day',
                'Publication_Time',
                'prediction'
            ]
            # Keeping only the relevant features
            merged_df = merged_df[cols_to_keep]
            
            # Renaming the "prediction" feature to "Listening_Time_minutes"
            merged_df.rename(columns={'prediction': 'Listening_Time_minutes'}, inplace=True)
            
            return merged_df
        
        except Exception as e:
            raise CustomException(e, sys)
    
    
    # Creating a method to detect data drift
    def detect_data_drift(self, save_report=True):
        '''
        This method detects whether this is any data drift in the features or target. The method
        will leverage the read_data_from_db method to read the data from the database.
        '''
        try:
            # Reading the training data and keeping only the relevant features
            train_df = pd.read_parquet(self.ingestion_config.train_data_path)
            cols_to_keep = [
                'Podcast_Name',
                'Episode_Length_minutes',
                'Genre',
                'Publication_Day',
                'Publication_Time',
                'Listening_Time_minutes'
            ]
            train_df = train_df[cols_to_keep]
            
            # Reading the data from the database
            db_df = self.read_data_from_db()
            
            # Defining the schema for the data
            schema = DataDefinition(
            numerical_columns=["Episode_Length_minutes"],
            categorical_columns=["Podcast_Name", "Genre", "Publication_Day", "Publication_Time"],
            regression=[Regression(target='Listening_Time_minutes')]
            )
            
            # Creating the dataset objects for the train 
            train_data = Dataset.from_pandas(train_df, data_definition=schema)
            db_data = Dataset.from_pandas(db_df, data_definition=schema)
            
            # Creating the report with DataDriftPreset
            report = Report(metrics=[
                DataDriftPreset()
            ])
            
            # Running the report
            my_eval = report.run(
                reference_data=train_data, 
                current_data=db_data
            )
            
            # Creating the report folder and saving the report if it does
            # not already exist.
            if save_report:
                os.makedirs(os.path.dirname(self.report_config.report_path), exist_ok=True)
                my_eval.save_html(self.report_config.report_path)
        
        except Exception as e:
            raise CustomException(e, sys)