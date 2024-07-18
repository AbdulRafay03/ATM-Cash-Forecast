import pandas as pd
import numpy as np
import warnings
import copy
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder
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
        
        self.labelEncoding()
        self.split_for_regression()
        self.split_for_time_series()
        logger.info('Dataframe ready for model training')

        self.Timeseries = [self.ts_df_train , self.ts_df_test]
        self.Regression = [self.R_xtrain , self.R_xtest , self.R_ytrain , self.R_ytest]
        

    def labelEncoding(self):
        le = LabelEncoder()
        ft = ['IsHoliday','HolidayType','DayOfWeek','Event' , 'Paydays']
        for i in ft:
            self.df[i] = le.fit_transform(self.df[i])

    def split_for_time_series(self):
        ts_df = copy.deepcopy(self.df)
        ts_df = ts_df.rename(columns={'RecTime': 'ds', 'TotalValue': 'y'})
        train_size = int(len(ts_df) * 0.8)
        self.ts_df_train = ts_df.iloc[:train_size]
        self.ts_df_test = ts_df.iloc[train_size:]
        print(ts_df.columns)
    def split_for_regression(self):
        R_df = copy.deepcopy(self.df)
        R_df.pop('RecTime')
        y = R_df.pop('TotalValue')
        self.R_xtrain , self.R_xtest , self.R_ytrain , self.R_ytest = train_test_split(R_df , y , train_size= 0.8)
        return [R_df , y]

