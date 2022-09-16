from backtesting import Backtest, Strategy #引入回測和交易策略功能
from backtesting.lib import crossover #引入判斷均線交會功能
from backtesting.test import SMA #引入繪製均線功能
import pandas as pd
import matplotlib.pyplot as plt
from talib import abstract
import numpy as np
df=pd.read_csv('data2.csv',index_col=0) #CSV檔案中若有缺漏，會使用內插法自動補值，不一定需要的功能
df.index = pd.DatetimeIndex(df.index)

#calculate KD signal with talib
df_tmp=df
df_tmp.rename(
    columns={
        'High':'high',
        'Low':'low',
        'Close':'close'
    },
    inplace=True
)#rename for talib
abstract.STOCH(df_tmp).plot(figsize=(16,8))
plt.show()
kd=abstract.STOCH(df_tmp)
kd.index=df_tmp.index
fnl_df=df_tmp.join(kd).dropna()
fnl_df.rename(columns = {'high':'High', 'low':'Low','close':'Close'}, inplace = True)
print(fnl_df)

def I_bypass(data): # bypass data in Strategy
    return data

class KDCross(Strategy):
    lower_bound = 20
    upper_bound = 80
    sl_ratio=99#前一天k棒收盤價的99%當作停損價
    def init(self):
        self.k = self.I(I_bypass, self.data.slowk) #K
        self.d = self.I(I_bypass, self.data.slowd) #D

    def next(self):
        if crossover(self.k, self.d) and self.k<self.lower_bound and self.d<self.lower_bound and not self.position: #long position
            self.buy(size=.99,sl=self.data.Close[-1]*self.sl_ratio/100)#前一天k棒收盤價的99%當作停損價
        elif crossover(self.d, self.k) and self.k>self.upper_bound and self.d>self.upper_bound:
            if self.position and self.position.is_long:
                self.position.close()
#run backtest
bt = Backtest(fnl_df, KDCross, cash=10000, commission=.002)
rslt = bt.run()
print(rslt)
