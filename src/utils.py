# Importing packages
import sys
import os
import json
from pathlib import Path
import pandas as pd
from datetime import datetime
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

# Creating a helper function to save the run parameters
def save_run_params(run_params:dict):
    '''
    This function saves the run parameters as a json file in the run_config folder. 
    ========================================================================================
    ---------------------
    Parameters:
    ---------------------
    run_params : dict - This is the dictionary containing the run parameters.
    
    ---------------------
    Returns:
    ---------------------
    Saves the run parameters as a json file into the run_config folder.
    ========================================================================================
    '''
    try:
        # Creating a variable to capture the current time
        now = datetime.now().strftime('%Y%m%d_%H-%M-%S')
        # Saving the run parameters in the run_config folder
        file_name = Path.cwd() / 'run_config' / f'run_params_{now}.json'
        with open(file_name, 'w') as file_obj:
            json.dump(run_params, file_obj)
    
    except Exception as e:
        raise CustomException(e, sys)

# Creating a helper function to load the run parameters
def load_run_params(directory='run_config'):
    '''
    This function loads the run parameters as a json file, which is present
    in the run_config folder. 
    ========================================================================================
    ---------------------
    Parameters:
    ---------------------
    directory : str - This is the name of the directory in which the run parameters json
    file is stored.
    
    ---------------------
    Returns:
    ---------------------
    run_parameters : json - This is the run parameters json file.
    ========================================================================================
    '''
    try:
        # Setting the path to the directory
        dir_path = Path.cwd() / directory
        
        # Listing the files
        json_files = os.listdir(dir_path)
        
        # Selecting the latest file
        latest_file = None
        latest_date = None
        for file_name in json_files:
            date_str = file_name.split('_')[2].split('.')[0]
            file_date = datetime.strptime(date_str, '%Y%m%d')
            if not latest_date or file_date > latest_date:
                latest_date = file_date
                latest_file = dir_path / file_name
        return latest_file
    
    except Exception as e:
        raise CustomException(e, sys)

# Creating a function to read a json file
def read_json_file(file_path:str):
    '''
    This function reads a JSON file and returns the contents of the file.
    ========================================================================================
    ---------------------
    Parameters:
    ---------------------
    file_path : str - This is the path to the run parameters json file.
    
    ---------------------
    Returns:
    ---------------------
    data : json - This is the contents of the JSON file.
    =========================================================================================
    '''
    try:
        # Reading the json file and returning its contents
        with open(file_path, 'r') as file_obj:
            data = json.load(file_obj)
        return data
    
    except Exception as e:
        raise CustomException(e, sys)

# Creating a function to fetch the current time
def get_current_time():
    '''
    This function fetches the current time and returns it in the format
    YYYY-MM-DD HH:MM:SS.
    ========================================================================================
    ---------------------
    Returns:
    ---------------------
    current_time : str - This is the current time in the format YYYY-MM-DD HH:MM:SS.
    =========================================================================================
    '''
    try:
        time = str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
        current_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        return current_time
    
    except Exception as e:
        raise CustomException(e, sys)
    
    