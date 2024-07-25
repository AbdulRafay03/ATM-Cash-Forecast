from Feature_Engineering import Features
from Preprocessing import preprocess
from Model import model
import warnings
warnings.filterwarnings('ignore')
from Logger import setup_logging

logger = setup_logging('Forecast.log')
ft = Features(Dataset_path=r"C:\Users\Shaikh Abdul Rafay\Desktop\cashInfo-1006.json" ,
              USD_Dataset_path= r"C:\Users\Shaikh Abdul Rafay\Downloads\USD_PKR Historical Data.csv", 
              info= False)
pre = preprocess(ft.df)
models = model(pre.Timeseries ,  pre.Regression , pre.df)
