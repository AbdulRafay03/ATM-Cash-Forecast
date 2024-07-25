import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objs as go
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')
from Logger import setup_logging

logger = setup_logging('Forecast.log')

class model():
    def __init__(self , Ts_df , R_df , comp_df):
        self.Ts_df = Ts_df
        self.R_df = R_df
        self.comp_df = comp_df

        self.prophet()
        self.GradBoost()

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


    def prophet(self):
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
        model.fit(self.Ts_df[0])

        future = model.make_future_dataframe(periods=len(self.Ts_df[1]))

        forecast = model.predict(future)
        y_pred = forecast['yhat'].iloc[-len(self.Ts_df[1]):].values
        self.evaluate(model , y_pred , TS = True)
        # self.plot_Forecast(model , forecast , self.comp_df['TotalValue']  )

    def GradBoost(self):
        from sklearn.ensemble import GradientBoostingRegressor

        gb = GradientBoostingRegressor()

        gb.fit(self.R_df[0]  , self.R_df[2])
        pred = gb.predict(self.R_df[1])
        
        self.evaluate(model ,pred  , TS = False)
        # pred_w = gb.predict(self.comp_df[0])
        # self.plot_Forecast(model ,pred_w, self.comp_df[1])



        
