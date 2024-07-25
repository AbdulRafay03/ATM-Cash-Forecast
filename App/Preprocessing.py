import pandas as pd
import numpy as np
import warnings
import copy
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder
import pickle

warnings.filterwarnings('ignore')
from Logger import setup_logging

logger = setup_logging('Forecast.log')

class preprocess():

    def __init__(self , df):
        self.df = df
        y1 = self.df.pop('Type1Count')
        y2 = self.df.pop('Type2Count')
        y3 = self.df.pop('Type3Count')
        y4 = self.df.pop('Type4Count')
        self.df.drop(['Type1Value', 'Type2Value', 'Type3Value', 'Type4Value' , 'TotalValue'] , inplace= True, axis= 1)
        self.labelEncoding()
        self.splits = self.split()

        logger.info('Dataframe ready for model training')

        

    def labelEncoding(self):

        ft = ['IsHoliday', 'HolidayType', 'DayOfWeek', 'Event', 'Paydays', 'HolidaySequence', 'IsWeekend', 'PartOfMonth']

        # Create a dictionary to store the fitted LabelEncoders
        label_encoders = {}

        # Fit the LabelEncoders and transform the features
        for feature in ft:
            le = LabelEncoder()
            self.df[feature] = le.fit_transform(self.df[feature])
            label_encoders[feature] = le

        with open('label_encoders.pkl', 'wb') as file:
            pickle.dump(label_encoders, file)

    def split(self):
        self.df = self.df.dropna()
        self.df.pop('RecTime')
        y = self.df.pop('TotalValueUSD')
        xtrain , xtest , ytrain , ytest = train_test_split(self.df , y , train_size= 0.85)
        return [xtrain , xtest , ytrain , ytest]

