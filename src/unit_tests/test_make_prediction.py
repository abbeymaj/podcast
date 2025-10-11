# Importing packages
import pytest
import pandas as pd
import datetime
from src.utils import get_current_time
from src.components.create_custom_data import CreateCustomData

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