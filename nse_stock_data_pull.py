# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 12:11:33 2017

@author: rkprajap
"""

import quandl
import datetime
import pandas as pd
import os
import logging
import urllib

#-------------------------
#Setup Configuration
#---------------------------
cur_dir = os.getcwd()
today = datetime.date.today()
FORMAT = '%(asctime)s - [%(levelname)s]: %(message)s'
log_file = 'log\\' + str(today) + '.log'
logging.basicConfig(format=FORMAT, filename=log_file, filemode='w', level=logging.DEBUG, datefmt='%d-%B-%Y %I:%M:%S %p')

Stocks_file = 'NSE_Stocks.xlsx'
quandl.ApiConfig.api_key = '3bzfePnoW_TsJy8xrXTT'

def get_stock_history(stock_code, start, end, first_time=False):    
    start = str(start.year) + '-' + str(start.month) + '-' + str(start.day)
    end = str(end.year) + '-' + str(end.month) + '-' + str(end.day)
    code = 'NSE/' + urllib.quote_plus(stock_code)
    data = quandl.get(code, start_date=start, end_date=end)
    filename = 'data\\'+stock_code+'.xlsx'
    if not os.path.isfile(filename) or first_time:
        data.to_excel(filename, sheet_name='Daily Data', index=True)
    else:
        old_data = pd.read_excel(filename, sheetname='Daily Data', header=0, index_col=0)
        
        data = old_data.append(data)
        data.to_excel(filename, sheet_name='Daily Data', index=True)


#------------------------
# Read stocks list
#-------------------------
try:
    NSE_stocks = pd.read_excel(Stocks_file, sheetname='Stocks', header=0)
#    NSE_stocks['LastAccessDate'] = today    
except:
    logging.error('Could not load stock list')

    
#------------------------
# Iterate over stocks
#-------------------------
#NSE_stocks[['LastAccessDate']] = NSE_stocks[['LastAccessDate']].astype(str)
for index, row in NSE_stocks.iterrows():
    end = today
#    end = datetime.date(2017, 2, 7)
    print 'Fetching data for:', row['NSE Code']
    try:        
        if pd.isnull(row['LastAccessDate']):
            start = datetime.datetime.now() - datetime.timedelta(days=2*365)
            get_stock_history(row['NSE Code'], start, end, True)
        else:
            start = row['LastAccessDate'] + datetime.timedelta(days=1)
            get_stock_history(row['NSE Code'], start, end)
        NSE_stocks.set_value(index, 'LastAccessDate', end)#.strftime("%d-%B-%Y"))
    except (RuntimeError, TypeError, NameError) as err:
        logging.error('Could not fetch data for ' + row['NSE Code'] + ' - ' + str(err))   
        print err

NSE_stocks.to_excel(Stocks_file, sheet_name='Stocks', index=False)


if __name__ == '__main__':
    pass

#To Do
#world market indexes
#http://online.wsj.com/mdc/public/page/2_3022-intlstkidx.html

