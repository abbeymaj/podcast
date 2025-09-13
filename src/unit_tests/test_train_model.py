# Importing packages
import os
import pytest
import pandas as pd
from sklearn.linear_model import BayesianRidge
from src.components.config_entity import CreateFeatureStoreConfig
from src.components.find_best_model import FindBestModel
from src.components.train_model import TrainModel

# Creating a module to fetch the transformed train dataset
@pytest.fixture(scope='module')
def fetch_train_dataset():
    feature_store = CreateFeatureStoreConfig()
    train_data = pd.read_parquet(feature_store.xform_train_data)
    X = train_data.copy().drop(labels=['Listening_Time_minutes'], axis=1)
    y = train_data['Listening_Time_minutes'].copy()
    return X, y

# Verifying whether the find best model class works as expected.
def test_find_best_model(fetch_train_dataset):
    X_train, y_train = fetch_train_dataset
    estimator = BayesianRidge()
    params = {
        'max_iter': [300, 400],
        'tol': [0.001, 0.0001]
    }
    bst = FindBestModel()
    best_model, best_params = bst.find_best_model(
        estimator=estimator,
        params=params,
        train_set=X_train,
        target_set=y_train,
        cv=3
    )
    assert best_model is not None
    assert best_params is not None

# Verifying whether the best_model is a BayesianRidge model and 
# best_params is a dictionary.
def test_find_model_params_type(fetch_train_dataset):
    X_train, y_train = fetch_train_dataset
    estimator = BayesianRidge()
    params = {
        'max_iter': [300, 400],
        'tol': [0.001, 0.0001]
    }
    bst = FindBestModel()
    best_model, best_params = bst.find_best_model(
        estimator=estimator,
        params=params,
        train_set=X_train,
        target_set=y_train,
        cv=3
    )
    assert isinstance(best_model, BayesianRidge)
    assert isinstance(best_params, dict)

# Verifying whether the train and test datasets are split into
# feature and target datasets
def test_create_feature_target_datasets():
    train_model = TrainModel()
    X_train, X_test, y_train, y_test = train_model.create_feature_target_sets()
    assert X_train is not None
    assert X_test is not None
    assert y_train is not None
    assert y_test is not None

# Verifying that best models are found and training is done as expected
def test_model_training():
    model = TrainModel()
    best_model, best_params, metric = model.initiate_model_training(make_prediction=True)
    assert best_model is not None
    assert best_params is not None
    assert metric is not None