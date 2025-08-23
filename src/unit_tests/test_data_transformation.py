# Importing packages
import pytest
import pandas as pd
from src.components.config_entity import DataIngestionConfig
from src.components.transform_data import TransformData
from src.utils import drop_zero_listening_time


# Creating a module to fetch the train dataset
@pytest.fixture(scope='module')
def train_dataset():
    ingestion_config = DataIngestionConfig()
    return ingestion_config.train_data_path

# Verifying that the any rows with listening time of 0 are dropped
def test_zero_listening_rows_dropped(train_dataset):
    df = pd.read_parquet(train_dataset)
    df_dropped = drop_zero_listening_time(df)
    df_dropped = df_dropped.loc[df_dropped.loc[:, 'Listening_Time_minutes']==0.0, :]
    assert df_dropped.shape[0] == 0

# Verify that the output after dropping rows with listening time of 0 
# is a pandas dataframe
def test_zero_listening_rows_dropped_output_is_pandas_dataframe(train_dataset):
    df = pd.read_parquet(train_dataset)
    df_dropped = drop_zero_listening_time(df)
    assert isinstance(df_dropped, pd.DataFrame)

# Verifying that the Publication Day and Publication time features can be 
# concatenated
def test_concatenate_publication_day_time(train_dataset):
    df = pd.read_parquet(train_dataset)
    transform = TransformData()
    df_concat = transform.generate_features(df)
    assert 'Pub_Day_Time' in list(df_concat.columns)

# Verifying that the Publication Day and Publication Time features are dropped
def test_publication_day_time_dropped(train_dataset):
    df = pd.read_parquet(train_dataset)
    transform = TransformData()
    df_concat = transform.generate_features(df)
    assert ['Publication_Day', 'Publication_Time'] not in list(df_concat.columns)