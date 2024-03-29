import pandas as pd
import yfinance as yf
import numpy as np

list_stocks = pd.read_csv("tickers_stocks.csv", sep=';').set_index("ticker")

marketCap = []

i=0

for stock in list_stocks.index:

    try:

        equity = yf.Ticker(stock)

        marketCap.append(equity.info['marketCap'])

    except:

        print("Não tem equity: ", stock)
        marketCap.append(np.nan)
    #dividends.append(equity.info['dividens'])
    i=i+1
    print(i)

list_stocks['marketCap'] = marketCap

list_stocks.dropna(inplace=True)

list_stocks.to_csv("tickers_fundamentals.csv")
