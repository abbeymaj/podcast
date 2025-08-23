# Importing packages
import os
from dataclasses import dataclass

# Creating a class to store the configuration for the data ingestion
@dataclass
class DataIngestionConfig():
    '''
    This class is used to store the data configuration for the data
    ingestion component.
    '''
    train_data_path : str = os.path.join('artifacts', 'train_data.parquet')
    test_data_path : str = os.path.join('artifacts', 'test_data.parquet')
    raw_data_path : str = 'https://github.com/abbeymaj80/my-ml-datasets/raw/refs/heads/master/project_datasets/podcast/podcast_train.parquet'
    

# Creating a class to store the preprocessor object 
@dataclass
class DataTransformationConfig():
    '''
    This class is used to store the preprocessor object for the data transformation
    process.
    '''
    preprocessor_obj_path : str = os.path.join('artifacts', 'preprocessor_obj.joblib')