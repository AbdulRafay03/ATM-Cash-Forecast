from Feature_Engineering import Features
from Preprocessing import preprocess
from Model import model
import warnings
warnings.filterwarnings('ignore')
from Logger import setup_logging

logger = setup_logging('Forecast.log')
ft = Features(path=r"C:\Users\Hp\Desktop\cashInfo-1006.json" , info= True)
pre = preprocess(ft.df)
models = model(pre.Timeseries ,  pre.Regression , pre.df)
