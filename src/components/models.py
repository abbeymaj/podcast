# Importing packages
from datetime import datetime, timezone
from src.components.create_app import db

# Creating a class to define the table to store the user entered data
class Data(db.Model):
    '''
    This class defines the table to store the data which is enter
    by the user on the web page.
    '''
    __tablename__ = 'data'
    
    id = db.Column(db.Integer, primary_key=True)
    Podcast_Name = db.Column(db.String(30), nullable=False)
    Episode_Length_minutes = db.Column(db.Float, nullable=False)
    Genre = db.Column(db.String(30), nullable=False)
    Publication_Day = db.Column(db.String(30), nullable=False)
    Publication_Time = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    preds = db.relationship('Predictions', backref='data', lazy=True)
    
    # Creating a method to return the string representation of the class.
    def __repr__(self):
        '''
        This method returns the string representations of the class
        '''
        return f"Data('{self.Podcast_Name}', '{self.Episode_Length_minutes}', '{self.Genre}', '{self.Publication_Day}', '{self.Publication_Time}')"
    

# Creating a class to define a table to store the predictions
class Predictions(db.Model):
    '''
    This class defines the table to store the predictions made by the model.
    '''
    __tablename__ = 'predictions'
    
    pred_id = db.Column(db.Integer, primary_key=True)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)
    prediction = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # Creating a method to return the string representation of the class.
    def __repr__(self):
        '''
        This method returns a string representation of the Prediction class.
        '''
        return f"Predictions('{self.prediction}')"