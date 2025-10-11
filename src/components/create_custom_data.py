# Importing packages
import sys
import pandas as pd
from src.utils import get_current_time
from src.exception import CustomException
from src.logger import logging

# Creating a class to create custom data based on user input
class CreateCustomData():
    '''
    This class is responsible for converting the user entered data into a pandas
    dataframe. The class contains two methods - a constructor and a method to 
    convert user entered data into a pandas dataframe. 
    The objective of the class is to transform the user entered data so that the
    data can be used to make predictions.
    '''
    # Creating the constructor for the class
    def __init__(
        self,
        podcast_name:str,
        episode_length:float,
        genre:str,
        publication_day:str,
        publication_time:str
        ):
        '''
        This is the constructor for the create custom data class.
        '''
        self.podcast_name = podcast_name
        self.episode_length = episode_length
        self.genre = genre
        self.publication_day = publication_day
        self.publication_time = publication_time
    
    # Creating a method to convert user entered data into a pandas dataframe
    def create_dataframe(self):
        '''
        This method takes the data input by the user and returns a dataframe. The method 
        converts the data, input by the user on the website, into a dictionary and then creates
        a pandas dataframe using the dictionary.
        ========================================================================================
        -----------------------
        Returns:
        -----------------------
        df : pandas dataframe - A pandas dataframe of the data entered by the user.
        ========================================================================================
        '''
        try:
            logging.info("Creating a dataframe from the user entered data.")
            
            # Fetching the current time
            current_time = get_current_time()
            
            # Converting the user entered data into a dictionary
            data = {
                'time': [current_time],
                'podcast_name': [self.podcast_name],
                'episode_length': [self.episode_length],
                'genre': [self.genre],
                'publication_day': [self.publication_day],
                'publication_time': [self.publication_time]
            }
            
            # Creating a pandas dataframe from the dictionary
            df = pd.DataFrame(data)
            
            logging.info("Successfully create a dataframe from the user entered data")
            
            return df
        
        except Exception as e:
            raise CustomException(e, sys)