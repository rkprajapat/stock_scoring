# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 23:30:28 2017

@author: rkprajap
"""
import os, datetime, logging
import pandas as pd
import glob
from bokeh.charts import BoxPlot, output_file, show


cur_dir = os.getcwd()
today = datetime.date.today()
FORMAT = '%(asctime)s - [%(levelname)s]: %(message)s'
log_file = 'log\\' + str(today) + '.log'
logging.basicConfig(format=FORMAT, filename=log_file, filemode='w', level=logging.DEBUG, datefmt='%d-%B-%Y %I:%M:%S %p')

data_files = glob.glob("data\\*.xlsx")

for f in data_files:
    stock_history = pd.read_excel(f, sheetname='Daily Data', header=0)
    SMA10 = pd.rolling_mean(stock_history['Close'], 10)
    SMA20 = pd.rolling_mean(stock_history['Close'], 20)
    SMA50 = pd.rolling_mean(stock_history['Close'], 50)
    stock_history['SMA10'] = SMA10
    stock_history['SMA20'] = SMA20
    stock_history['SMA50'] = SMA50

