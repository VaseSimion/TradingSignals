import mplfinance as mpf
import numpy as np
import pandas as pd
import tulipy as ti
import yfinance as yf

stock = "RILY"
ticker_handle = yf.Ticker(stock)

history = ticker_handle.history(interval="1wk", period="2y", threads=False)
history.dropna(subset=["Close"], inplace=True)

print(ticker_handle.earnings)
print(ticker_handle.quarterly_earnings)
#Gf.draw_macd_buy(history, stock)

sma = list(ti.sma(np.array(history["Close"].tolist()), period=5))
df_sma = pd.DataFrame(index=history.index.tolist(), data=[float("nan")]*4 + sma)

close_list = history["Close"]
processed_min = [float("nan"), float("nan")]
processed_max = [float("nan"), float("nan")]
last_found = ("none", 0)
last_value = 0

for index, element in enumerate(close_list[2:-2]):
    if (close_list[index+1] > element < close_list[index+3]) and (close_list[index] > element < close_list[index+4]) \
            and (abs((element - last_value)/element) > 0.03):
        processed_min += [element]
        last_value = element
        if last_found[0] == "min":
            processed_min[last_found[1]+2] = float("nan")
            last_found = ("min", index)
        else:
            last_found=("min", index)
    else:
        processed_min += [float("nan")]

    if (close_list[index+1] < element > close_list[index+3]) and (close_list[index] < element > close_list[index+4]) \
            and (abs((element - last_value)/element) > 0.03):
        processed_max += [element]
        last_value = element
        if last_found[0] == "max":
            processed_max[last_found[1] + 2] = float("nan")
            last_found = ("max", index)
        else:
            last_found = ("max", index)
    else:
        processed_max += [float("nan")]

processed_min += [float("nan"), float("nan")]
processed_max += [float("nan"), float("nan")]


df_close_min = pd.DataFrame(index=history.index.tolist(), data=processed_min)
df_close_max = pd.DataFrame(index=history.index.tolist(), data=processed_max)

ap = [mpf.make_addplot(df_close_min, type="scatter", markersize=100, marker='^'),
      mpf.make_addplot(df_close_max, type="scatter", markersize=100, marker='v')]
mpf.plot(history, type="line", volume=True, addplot=ap)#, savefig='testsave.png')