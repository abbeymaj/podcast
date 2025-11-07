## Predicting Time Spent Listening to a Podcast

The objective of this project is to predict the number of minutes a user will spend listening to a podcast, given the podcast name, genre, episode length and publication day & time. This problem is a regression problem.

## Installation

Install the project using pip. It is always recommended to use a virtual environment (for example, using anaconda) to do the installation.

This project was built using Python 3.9.

To install the project, use the following: 

```bash
  pip install -r requirements.txt
```
    
## Tech Stack

**Client:** Flask, HTML, CSS

**Language:** Python

**Model Registry:** MLflow

## Screenshots of the Prediction Website 

There are two webpages, which the user can interact with, for the project. 

Landing Page:

This is the landing page for the project. The page provides a brief overview of the project and then allows the user to navigate to the prediction page. 

The screenshot of the Landing Page is given below:

![Landing Page Screenshot Link](https://github.com/abbeymaj80/my-ml-datasets/blob/master/screenshots/Podcast_Landing_Page.png)

Prediction Page:

The prediction page enables the user to select or enter information that allows a user to select podcast name, genre, episode length and publication day & time. This information will be used to predict the number of minutes a user will spend listening to the podcast. Once the user enters the necessary information, the user must click on the "Predict" button to generate the prediction.

The screenshot of the Prediction page is given below:

![Prediction page Screenshot Link](https://github.com/abbeymaj80/my-ml-datasets/blob/master/screenshots/Podcast_Prediction_Page.png)