# Importing packages
import pandas as pd
import pytest
from src.components.detect_drift import DetectDataDrift

# Verifying that the read_data_from_db method works as expected
def test_read_data_from_db_method():
    drift = DetectDataDrift()
    df = drift.read_data_from_db()
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 0

# Verifying that only the relevant features are returned
def test_important_features_in_df():
    drift = DetectDataDrift()
    df = drift.read_data_from_db()
    cols_to_keep = [
        'Podcast_Name',
        'Episode_Length_minutes',
        'Genre',
        'Publication_Day',
        'Publication_Time',
        'Listening_Time_minutes'
    ]
    assert all(feature in list(df.columns) for feature in cols_to_keep)

# Verifying that the target feature was renamed to "Listening_Time_minutes"
def test_target_feature_renamed():
    drift = DetectDataDrift()
    df = drift.read_data_from_db()
    assert 'prediction' not in list(df.columns)
    assert 'Listening_Time_minutes' in list(df.columns)

# Verifying that the detect_data_drift method works as expected
def test_detect_data_drift_method():
    temp_drift = DetectDataDrift()
    temp_drift.detect_data_drift(save_report=False)