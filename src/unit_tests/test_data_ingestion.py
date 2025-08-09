# Importing packages
import os
import pytest
import pandas as pd
from src.components.config_entity import DataIngestionConfig
from src.components.data_ingestion import DataIngestion


# Creating a module for the train dataset
@pytest.fixture(scope='module')
def train_dataset():
    ingestion_config = DataIngestionConfig()
    return ingestion_config.train_data_path

# Creating a module for the test dataset
@pytest.fixture(scope='module')
def test_dataset():
    ingestion_config = DataIngestionConfig()
    return ingestion_config.test_data_path

# Verifying that the raw data is available
def test_raw_data_is_available():
    ingestion_config = DataIngestionConfig()
    raw_data_path = ingestion_config.raw_data_path
    df = pd.read_parquet(raw_data_path)
    assert df.shape[0] > 0
    assert df.shape[1] > 1
    
# Verifying that the artifacts folder was created
def test_artifacts_folder_created():
    assert os.path.exists('artifacts') is True

# Verifying that the train dataset was created
def test_created_train_dataset(train_dataset):
    assert os.path.exists(train_dataset) is True

# Verifying that the test dataset was created
def test_created_test_dataset(test_dataset):
    assert os.path.exists(test_dataset) is True

# Verifying that the train dataset is not empty
def test_train_dataset_not_empty(train_dataset):
    assert os.path.getsize(train_dataset) > 0

# Verifying that the test dataset is not empty
def test_test_dataset_not_empty(test_dataset):
    assert os.path.getsize(test_dataset) > 0

# Verifying that the train dataset does not contain dropped features
def test_train_dataset_does_not_contain_dropped_features(train_dataset):
    dropped_features = [
        'id',
        'Episode_Title',
        'Host_Popularity_percentage',
        'Guest_Popularity_percentage',
        'Number_of_Ads',
        'Episode_Sentiment'
    ]
    df = pd.read_parquet(train_dataset)
    assert all(feature not in list(df.columns) for feature in dropped_features)

# Verifying that the test dataset does not contain dropped features
def test_test_dataset_does_not_contain_dropped_features(test_dataset):
    dropped_features = [
        'id',
        'Episode_Title',
        'Host_Popularity_percentage',
        'Guest_Popularity_percentage',
        'Number_of_Ads',
        'Episode_Sentiment'
    ]
    df = pd.read_parquet(test_dataset)
    assert all(feature not in list(df.columns) for feature in dropped_features)