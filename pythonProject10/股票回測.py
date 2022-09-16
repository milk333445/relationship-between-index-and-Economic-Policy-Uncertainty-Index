import yfinance as yf
import pandas as pd
from pandas_datareader import data
from datetime import datetime

yf.pdr_override()

target_stock='2330.TW'
start_date=datetime(2019,1,2)
end_date=datetime(2022,7,23)
df=data.get_data_yahoo([target_stock],start_date,end_date)
df.to_csv('data2.csv')
print(df)