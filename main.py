# BOLLINGER BANDS


import yfinance as yf
import pandas as pd
import numpy as np
import ta
from ta.momentum import RSIIndicator
import matplotlib.pyplot as plt

df = yf.download('SQ', start='2019-01-01')

df['ma_20'] = df.Close.rolling(20).mean()
df['vol'] = df.Close.rolling(20).std()
df['upper_bb'] = df.ma_20 + (2 * df.vol)
df['lower_bb'] = df.ma_20 - (2 * df.vol)

df_plot = df[['Close', 'ma_20', 'upper_bb', 'lower_bb']]

df['rsi'] = ta.momentum.rsi(df.Close, window=6)

conditions = [(df.rsi < 30) & (df.Close < df.lower_bb), (df.rsi > 70) & (df.Close > df.upper_bb)]

choices = ['Buy', 'Sell']

df['signal'] = np.select(conditions, choices)

df.signal = df.signal.shift()
df.dropna(inplace=True)

position = False

buydates, selldates = [], []
buyprices, sellprices = [], []

for index, row in df.iterrows():
    if not position and row['signal'] == 'Buy':
        buydates.append(index)
        buyprices.append(row.Open)
        position = True

    if position and row['signal'] == 'Sell':
        selldates.append(index)
        sellprices.append(row.Open)
        position = False

plt.plot(df.Close)
plt.scatter(df.loc[buydates].index, df.loc[buydates].Close, marker='^', c='g')
plt.scatter(df.loc[selldates].index, df.loc[selldates].Close, marker='^', c='r')
# plt.figure(figsize=(10,5))
# plt.show()

# P&L

pnl = (pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) +1).prod()-1
print(pnl)
