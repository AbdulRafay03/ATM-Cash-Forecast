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
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
import pickle
from sklearn.preprocessing import LabelEncoder

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

        logger.info('Build_Models...')

        preds = self.Build_models()

        self.evaluate(preds)
        



    def Build_models(self):
        gb = GradientBoostingRegressor(learning_rate =  0.01687770422304368,
            max_depth = 3,min_samples_leaf = 4,
            min_samples_split = 19,n_estimators = 409,
            subsample = 0.8776807051588262)
        lgbm= lgb.LGBMRegressor(subsample=0.9,num_leaves=31,
            n_estimators=500,min_child_samples=40,
            learning_rate=0.01,colsample_bytree=0.7, verbosity = -1
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


        #Stacked_Regressor
        base_models = [
            ('rf', RandomForestRegressor(bootstrap=True,max_depth=19,
                max_features='auto',min_samples_leaf=9,
                min_samples_split=13,n_estimators=314
            )),
            ('gb', GradientBoostingRegressor(learning_rate=0.01687770422304368,max_depth=3,
                min_samples_leaf=4,min_samples_split=19,
                n_estimators=409,subsample=0.8776807051588262
            )),
            ('xgb', XGBRegressor(colsample_bytree=0.7845407345828739,
                gamma=0.06351182959000135,learning_rate=0.017364373527198277,
                max_depth=3,min_child_weight=5,
                n_estimators=360,subsample=0.9323611881275267
            )),
            ('catboost', CatBoostRegressor(learning_rate=0.01,
                l2_leaf_reg=3,iterations=1000,
                depth=4,verbose=0
            )),
            ('lgbm', lgb.LGBMRegressor(subsample=0.9,num_leaves=31,
                n_estimators=500,min_child_samples=40,
                learning_rate=0.01,colsample_bytree=0.7  ,verbosity=-1
            ))
        ]
        # Define meta-model
        meta_model = LinearRegression()
        # Create Stacking Regressor
        sr = StackingRegressor(
            estimators=base_models,
            final_estimator=meta_model
        )
        preds = []
        for i in [gb , lgbm , cb , rf , xgb , sr]:
            i.fit(self.xtrain , self.ytrain)
            preds.append(i.predict(self.xtest))
        

        self.models_list = [gb , lgbm , cb , xgb, rf , sr]

        return preds


    def evaluate(self , preds):
      
        preds.append(np.mean(preds, axis=0))
        preds.append(np.max(preds, axis=0))
        models = [
            'Gradient Boost',
            'LightGBM',
            'CatBoost',
            'Random Forest',
            'XGBoost',
            'Stacked Reg',
            'Average',
            'Max'
        ]

        # List to store the evaluation metrics
        metrics = []

        # Calculate and store metrics for each model
        for var_name, predictions in zip(models , preds):
            mse = mean_squared_error(self.ytest, predictions)
            mae = mean_absolute_error(self.ytest, predictions)
            mape = mean_absolute_percentage_error(self.ytest, predictions)
            r2 = r2_score(self.ytest, predictions)
            
            metrics.append({
                'Model': var_name,
                'MSE': mse,
                'MAE': mae,
                'MAPE': mape,
                'R²': r2
            })

        metrics_df = pd.DataFrame(metrics)

        metrics_df_sorted = metrics_df.sort_values(by='MAE')

        top_model_metrics = metrics_df_sorted.iloc[0]
        
        logger.info(top_model_metrics)
        
    def infer(self ,entry):
        with open('label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)

        
        for feature in entry:
            print(feature)
            value = entry[feature]
            if feature in label_encoders:
                value = label_encoders[feature].transform([value])[0]
            entry[feature] = value
        

        ent = pd.DataFrame([entry])

        ent['Year'] = ent['Year'].astype(int)
        ent['Month'] = ent['Month'].astype(int)
        ent['Date'] = ent['Date'].astype(int)
        ent['Quarter'] = ent['Quarter'].astype(int)
        ent['DayOfYear'] = ent['DayOfYear'].astype(int)
        ent['Last7Days_mean'] = ent['Last7Days_mean'].astype(float)
        ent['Last30Days_mean'] = ent['Last30Days_mean'].astype(float)
        ent['Difference'] = ent['Difference'].astype(float)
        
        pp = []
        for m in self.models_list:
            pp.append(m.predict(ent))
        

        return pp



                





            
            


        
