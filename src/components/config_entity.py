# Importing packages
import os
from datetime import datetime
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

# Creating a class to define the feature store and store the transformed datasets
@dataclass
class CreateFeatureStoreConfig():
    '''
    This class defines the path to the feature store, which contains the transformed
    datasets.
    '''
    xform_train_data : str = os.path.join('feature_store', 'xform_train_data.parquet')
    xform_test_data : str = os.path.join('feature_store', 'xform_test_data.parquet')


# Creating a class to store the model
@dataclass
class ModelTrainerConfig():
    '''
    This class defines the path to artifact folder where the model is stored.
    '''
    model_path : str = os.path.join('artifacts', 'model.joblib')
    
# Creating a class to store the mlflow model uri path
@dataclass
class ModelURIConfig():
    '''
    This class defines the path to the mlflow tracking uri.
    '''
    model_uri : str = 'https://dagshub.com/abbeymaj/podcast.mlflow'

# Creating a class to store the path to the SQLite database
@dataclass
class DatabaseConfig():
    '''
    This class stores the path to the SQLite database.
    '''
    db_path : str = os.path.join('db', 'podcast.db')

# Creating a class to store the path to the drift detection report
@dataclass
class DriftDetectorConfig():
    '''
    This class stores the path to the drift detection report.
    '''
    current_date = datetime.now().strftime('%Y_%m_%d')
    report_name = current_date + '_drift_report.html'
    report_path : str = os.path.join('reports', report_name)