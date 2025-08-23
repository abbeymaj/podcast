# Importing packages
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException

# Creating a function to drop all rows that have a listing time of 0
def drop_zero_listening_time(df:pd.DataFrame)->pd.DataFrame:
    '''
    This function drops any row where the listening time for the podcast
    is 0. The function accepts a Pandas dataframe as an argument and 
    returns a Pandas dataframe.
    =========================================================================
    -------------------
    Parameters:
    -------------------
    df : Pandas Dataframe - This is the dataframe with the raw data.
    
    -------------------
    Returns:
    -------------------
    df : Pandas Dataframe - This is the dataframe with the rows dropped.
    =========================================================================
    '''
    try:
        logging.info('Dropping rows with listening time of 0.')
        
        # Setting a mask to only take rows where listening time is greater
        # than 0.
        df_zero = df.loc[:, 'Listening_Time_minutes'] > 0.0
        
        # Filtering the dataframe with the rows that have a listening time
        # grater than 0.
        df_without_zero = df[df_zero]
        
        logging.info('Successfully dropped rows with listening time of 0.')
        
        return df_without_zero
    
    except Exception as e:
        raise CustomException(e, sys)
    