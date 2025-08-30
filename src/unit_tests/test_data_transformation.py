# Importing packages
import os
import pytest
import pandas as pd
import sklearn
from src.components.config_entity import DataIngestionConfig
from src.components.config_entity import DataTransformationConfig
from src.components.config_entity import CreateFeatureStoreConfig
from src.components.transform_data import TransformData
from src.utils import drop_zero_listening_time


# Creating a module to fetch the train dataset
@pytest.fixture(scope='module')
def train_dataset():
    ingestion_config = DataIngestionConfig()
    return ingestion_config.train_data_path

# Creating a module to fetch the test dataset
@pytest.fixture(scope='module')
def test_dataset():
    ingestion_config = DataIngestionConfig()
    return ingestion_config.test_data_path

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

# Verifying that the "Listening_Time_minutes" feature is present in the dataset
def test_target_feature_not_present(train_dataset):
    df = pd.read_parquet(train_dataset)
    X = df.copy().drop(labels=['Listening_Time_minutes'], axis=1)
    y = df['Listening_Time_minutes'].copy()
    transform = TransformData()
    df_concat = transform.generate_features(X)
    assert ['Listening_Time_minutes'] not in list(df_concat.columns)

# Verifying that the data transformation process works as expected
def test_initiate_data_transformation(train_dataset, test_dataset):
    df_train = pd.read_parquet(train_dataset)
    df_test = pd.read_parquet(test_dataset)
    transform = TransformData()
    train_arr, test_arr, preprocessor_obj = transform.initiate_data_transformation(df_train, df_test, save_object=False)
    assert isinstance(train_arr, pd.DataFrame)
    assert isinstance(test_arr, pd.DataFrame)
    assert isinstance(preprocessor_obj, sklearn.compose._column_transformer.ColumnTransformer)

# Verifying that the preprocessor object was saved in the artifacts folder
def test_preprocessor_obj_saved():
    transform_config = DataTransformationConfig()
    assert os.path.exists(transform_config.preprocessor_obj_path) is True

# Verify that the feature store folder was created
def test_feature_store_folder_created():
    feature_store_config = CreateFeatureStoreConfig()
    assert os.path.exists(os.path.dirname(feature_store_config.xform_train_data)) is True

# Verify that the transformed train dataset was stored in the feature store folder
def test_transformed_train_dataset_created():
    feature_store_config = CreateFeatureStoreConfig()
    assert os.path.exists(feature_store_config.xform_train_data) is True

# Verify that the transformed test dataset was stored in the feature store folder
def test_transformed_test_dataset_created():
    feature_store_config = CreateFeatureStoreConfig()
    assert os.path.exists(feature_store_config.xform_test_data) is True

# Verify that the transformed train dataset is not empty
def test_transformed_train_dataset_not_empty():
    feature_store_config = CreateFeatureStoreConfig()
    assert os.path.getsize(feature_store_config.xform_train_data) > 0

# Verify that the transformed test dataset is not empty
def test_transformed_test_dataset_not_empty():
    feature_store_config = CreateFeatureStoreConfig()
    assert os.path.getsize(feature_store_config.xform_test_data) > 0