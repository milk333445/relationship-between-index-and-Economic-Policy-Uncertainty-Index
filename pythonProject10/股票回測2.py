from backtesting import Backtest, Strategy #引入回測和交易策略功能

from backtesting.lib import crossover #引入判斷均線交會功能
from backtesting.test import SMA #引入繪製均線功能

import pandas as pd #引入pandas讀取股價歷史資料CSV檔

class SmaCross(Strategy): #交易策略命名為SmaClass，使用backtesting.py的Strategy功能
    n1 = 5 #設定第一條均線日數為5日(周線)
    n2 = 20 #設定第二條均線日數為20日(月線)，這邊的日數可自由調整

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1) #定義第一條均線為sma1，使用backtesting.py的SMA功能算繪
        self.sma2 = self.I(SMA, self.data.Close, self.n2) #定義第二條均線為sma2，使用backtesting.py的SMA功能算繪

    def next(self):
        if crossover(self.sma1, self.sma2): #如果周線衝上月線，表示近期是上漲的，則買入
            self.buy()
        elif crossover(self.sma2, self.sma1): #如果周線再與月線交叉，表示開始下跌了，則賣出
            self.position.close()
df=pd.read_csv('data2.csv',index_col=0) #CSV檔案中若有缺漏，會使用內插法自動補值，不一定需要的功能
df.index = pd.DatetimeIndex(df.index)
print(df)
#回測功能
test = Backtest(df, SmaCross, cash=10000, commission=0.004)
# (資料來源、策略、現金、手續費)

result = test.run()
opt_result=test.optimize(
    n1=range(5,50,5),
    n2=range(10,120,5),
    maximize='SQN',
    constraint=lambda p:p.n1 < p.n2
)

print('Original strategy')
print(result)
print()
print("Optimize strategy")
print(opt_result)

