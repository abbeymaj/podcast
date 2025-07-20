# Importing packages
from typing import List
from setuptools import find_packages, setup

# Creating a Global Variable for the -e . in requirements
HYPHEN_E_DOT = '-e .'

# Creating a function to fetch all packages from the requirements.txt document
def fetch_packages(file_path:str) -> List[str]:
    '''
    This function will return the list of packages that are specified in the 
    requirements file.
    ==========================================================================
    ---------------
    Parameters:
    ---------------
    file_path : str : This is the path to the requirements.txt file.
    
    ---------------
    Returns:
    ---------------
    List - List[str] - This is the list of packages that need to be installed
    for the project, which is specified in the requirements.txt file.
    ==========================================================================
    '''
    # Creating an empty list to store the package names
    requirements = []
    
    # Reading the packages from requirements.txt
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        
        # Removing any line characters and replacing with blank spaces
        requirements = [req.replace('\n', "") for req in requirements]
        
        # Removing the -e . from the requirements list
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements

# Creating the setup to install all packages from the requirements.txt document
setup(
    name='Podcast Listening Prediction',
    version='0.0.1',
    author='Abhijit Majumdar',
    packages=find_packages(),
    install_requires=fetch_packages('requirements.txt')
)