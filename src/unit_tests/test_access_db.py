# Importing packages
import os
import pytest
import pandas as pd
import sqlite3
from src.components.config_entity import DatabaseConfig
from src.utils import read_sql_data

# Verifying that the database can be accessed
def test_db_path_exists():
    db_config = DatabaseConfig()
    assert os.path.exists(db_config.db_path)

# Verifying that the database can be read
def test_read_db():
    db_config = DatabaseConfig()
    db_path = db_config.db_path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()
    assert len(rows) > 0
    conn.close()
    
# Verifying that the read_sql data function works as expected
# to read the data from the data table
def test_read_sql_data_function():
    df = read_sql_data(table='data')
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 0

# Verifying tha the read_sql_data function works as expected
# to read the data from the predictions table
def test_read_sql_data_predictions_function():
    df = read_sql_data(table='predictions')
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 0

# Verifying that both tables can be read and joined
def test_join_tables():
    data_df = read_sql_data(table='data')
    preds_df = read_sql_data(table='predictions')
    merged_df = data_df.merge(preds_df, left_on='id', right_on='data_id', how='left')
    assert merged_df is not None
    assert isinstance(merged_df, pd.DataFrame)
    assert merged_df.shape[0] > 0
    assert merged_df.shape[1] > 0