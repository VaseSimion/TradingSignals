import mplfinance as mpf
import numpy as np
import pandas as pd
import tulipy as ti
import yfinance as yf
import AnalysisModule as As
import GraphFunctions as Gf

stock = "SBLK"
ticker_handle = yf.Ticker(stock)

history = ticker_handle.history(interval="1d", period="2y", threads=False)
history.dropna(subset=["Close"], inplace=True)

print(ticker_handle.earnings)
print(ticker_handle.quarterly_earnings)
#Gf.draw_macd_buy(history, stock)

sma = list(ti.sma(np.array(history["Close"].tolist()), period=5))
df_sma = pd.DataFrame(index=history.index.tolist(), data=[float("nan")]*4 + sma)

print(As.is_stock_uptrend(history))
print(As.is_breaking_out_of_base(history))
print(As.is_cup_and_hadle(history))
#Gf.draw_minmax(history)
Gf.draw_minmax_on_filtered(history)
