from backtesting import Backtest, Strategy 
from backtesting.lib import crossover
from backtesting.test import SMA 
import talib
import pandas as pd

class OneMA(Strategy):
    n1=60 #預設均線參數

    def init(self):
        self.sma1=self.I(SMA,self.data.Close,self.n1)
    def next(self):
        if (self.data.Close>self.sma1) and (not self.position.is_long):#如果收盤價>sma1(也就是60ma)，而且目前沒有多單部位
            self.buy()
        elif (self.data.Close<self.sma1):
            self.position.close()
df=pd.read_csv('data2.csv',index_col=0) #CSV檔案中若有缺漏，會使用內插法自動補值，不一定需要的功能
df.index = pd.DatetimeIndex(df.index)
print(df)
bt=Backtest(df,OneMA,cash=10000,commission=0.002)
stats=bt.optimize(n1=range(2,241,1),maximize='Equity Final [$]')#這邊會將均線參數從2~240去跑跑看這239個參數中哪一個能讓最後帳戶總淨值最高
print(stats)