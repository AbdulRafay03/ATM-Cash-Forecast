import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import StackingRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import warnings
warnings.filterwarnings('ignore')
from Logger import setup_logging

logger = setup_logging('Forecast.log')

class model():
    def __init__(self ,splits ):
        self.xtrain = splits[0]
        self.xtest = splits[1]
        self.ytrain = splits[2]
        self.ytest = splits[3]

        
        self.()

    def evaluate(self ,model , y_pred , TS):
        if TS:
            
            mae = mean_absolute_error(self.Ts_df[1]['y'], y_pred)
            mse = mean_squared_error(self.Ts_df[1]['y'], y_pred)
            rmse = np.sqrt(mse)

        else:   
            mae = mean_absolute_error(self.R_df[3], y_pred)
            mse = mean_squared_error(self.R_df[3], y_pred)
            rmse = np.sqrt(mse)

        logger.info(f'Model : {model.__class__.__name__} ')
        logger.info(f'Mean Absolute Error (MAE): {mae:.2f}')
        logger.info(f'Mean Squared Error (MSE): {mse:.2f}')
        logger.info(f'Root Mean Squared Error (RMSE): {rmse:.2f}')

    def plot_Forecast(self,model, y_pred , y_true):
        fig = make_subplots(rows=1, cols=1)

        # Add true values trace
        fig.add_trace(
            go.Scatter(x=self.Ts_df['ds'], y=y_true, mode='lines', name='True Values', line=dict(color='blue')),
            row=1, col=1
        )

        # Add predicted values trace
        fig.add_trace(
            go.Scatter(x=self.Ts_df['ds'], y=y_pred, mode='lines', name='Predicted Values', line=dict(color='red', dash='dash')),
            row=1, col=1
        )

        # Update layout
        fig.update_layout(
            title=f'{model.__class__.__name__} True vs Predicted Values ',
            xaxis_title='Date',
            yaxis_title='Values',
            legend=dict(x=0, y=1.0)
        )
        fig.show()
        # fig.write_image(f"{model.__class__.__name__}fig.png")

    def fit_models():
        gb = GradientBoostingRegressor(learning_rate =  0.01687770422304368,
            max_depth = 3,min_samples_leaf = 4,
            min_samples_split = 19,n_estimators = 409,
            subsample = 0.8776807051588262)
        lgbm= lgb.LGBMRegressor(subsample=0.9,num_leaves=31,
            n_estimators=500,min_child_samples=40,
            learning_rate=0.01,colsample_bytree=0.7
        )
        cb = CatBoostRegressor(learning_rate=0.01,l2_leaf_reg=3,
            iterations=1000,depth=4,verbose=0
        )
        rf = RandomForestRegressor(bootstrap=True,max_depth=19,
            max_features='auto',min_samples_leaf=9,
            min_samples_split=13,n_estimators=314
        )
        xgb = XGBRegressor(colsample_bytree=0.7845407345828739,gamma=0.06351182959000135,
            learning_rate=0.017364373527198277,max_depth=3,
            min_child_weight=5,n_estimators=360,
            subsample=0.9323611881275267
        )

    
    


        
