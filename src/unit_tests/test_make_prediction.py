# Importing packages
import pytest
import pandas as pd
import datetime
from src.utils import get_current_time
from src.components.create_custom_data import CreateCustomData
from src.components.make_predictions import MakePredictions

# Verifying that the current time is returned in the correct format
def test_get_current_time():
    time = get_current_time()
    assert time is not None
    assert isinstance(time, datetime.datetime)

# Verifying that the create custom data class works as expected
def test_create_custom_data():
    data_dict = {
        'podcast_name': 'test',
        'episode_length': 60.0,
        'genre': 'test_genre',
        'publication_day': 'Monday',
        'publication_time': '08:00:00'
    }
    custom_data = CreateCustomData(**data_dict)
    df = custom_data.create_dataframe()
    assert df is not None
    assert isinstance(df, pd.DataFrame)

# Verifying that the run params can be fetched correctly
def test_fetch_model_params():
    make_pred = MakePredictions()
    runs_data, latest_model_uri = make_pred.fetch_model_params()
    assert runs_data is not None
    assert latest_model_uri is not None

# Verifying that the model can be fetched from the model registry
def test_fetch_latest_model():
    make_pred = MakePredictions()
    model = make_pred.fetch_latest_model()
    assert model is not None