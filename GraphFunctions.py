import numpy as np
import tulipy as ti
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import AnalysisModule as As
import mplfinance as mpf
import pandas as pd

def draw_macd_buy(stock, name):
    closing_price_list = stock['Close'].tolist()
    date_list = list(stock.index)

    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 8, 17, 9)  # for buy signals it should be 8,17,9
    sma = ti.sma(numpyclose, 17)

    plt.figure(figsize=(15, 8))
    ax1 = plt.subplot(212)
    ax2 = plt.subplot(211, sharex=ax1, title=name)
    numberofactivedays = len(date_list[16:])
    arrangeddates = np.arange(numberofactivedays)
    ax1.plot(arrangeddates, macd1, 'r')
    ax1.plot(arrangeddates, macd2, 'y')
    ax1.bar(arrangeddates, macdhistogram)
    ax1.plot(arrangeddates, [0] * len(date_list[16:]))
    ax2.plot(arrangeddates, closing_price_list[16:])
    ax2.plot(arrangeddates, sma, 'r')
    ax1.set_xticks(np.append(arrangeddates[0::20], arrangeddates[-1]))
    ax2.set_xticks(np.append(arrangeddates[0::20], arrangeddates[-1]))
    ax1.set_xticklabels([date.strftime("%Y-%m-%d") for date in date_list[16:]][0::20] +
                        [[date.strftime("%Y-%m-%d") for date in date_list[16:]][-1]])
    ax2.set_xticklabels([date.strftime("%Y-%m-%d") for date in date_list[16:]][0::20] +
                        [[date.strftime("%Y-%m-%d") for date in date_list[16:]][-1]])
    ax1.tick_params(rotation=30)
    ax2.tick_params(rotation=30)
    plt.show()


def save_macd_buy(stock, name):
    closing_price_list = stock['Close'].tolist()
    date_list = list(stock.index)

    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 8, 17, 9)  # for buy signals it should be 8,17,9
    sma = ti.sma(numpyclose, 17)

    plt.figure(figsize=(15, 8))
    ax1 = plt.subplot(212)
    ax2 = plt.subplot(211, sharex=ax1, title=name)
    numberofactivedays = len(date_list[16:])
    arrangeddates = np.arange(numberofactivedays)
    ax1.plot(arrangeddates, macd1, 'r')
    ax1.plot(arrangeddates, macd2, 'y')
    ax1.bar(arrangeddates, macdhistogram)
    ax1.plot(arrangeddates, [0] * len(date_list[16:]))
    ax1.set(ylabel='MACD')
    ax2.plot(arrangeddates, closing_price_list[16:])
    ax2.plot(arrangeddates, sma, 'r')
    ax2.set(ylabel="Price")

    ax1.set_xticks(np.append(arrangeddates[0::20], arrangeddates[-1]))
    ax2.set_xticks(np.append(arrangeddates[0::20], arrangeddates[-1]))
    ax1.set_xticklabels([date.strftime("%Y-%m-%d") for date in date_list[16:]][0::20] +
                        [[date.strftime("%Y-%m-%d") for date in date_list[16:]][-1]])
    ax2.set_xticklabels([date.strftime("%Y-%m-%d") for date in date_list[16:]][0::20] +
                        [[date.strftime("%Y-%m-%d") for date in date_list[16:]][-1]])
    ax1.tick_params(rotation=30)
    ax2.tick_params(rotation=30)
    plt.savefig("Reports/Support Files For Pdf/" + name + ".png")
    plt.close()


def draw_minmax(stock_history, save=False, title="Default", save_name="testsave.png"):
    [processed_min, processed_max] = As.return_last_minimums_maximum_sell(stock_history)

    df_close_min = pd.DataFrame(index=stock_history.index.tolist(), data=processed_min)
    df_close_max = pd.DataFrame(index=stock_history.index.tolist(), data=processed_max)

    ap = [mpf.make_addplot(df_close_min, type="scatter", markersize=100, marker='^'),
          mpf.make_addplot(df_close_max, type="scatter", markersize=100, marker='v')]
    if save:
        mpf.plot(stock_history, type="line", volume=True, addplot=ap, title=title, savefig=save_name)
    else:
        mpf.plot(stock_history, type="line", volume=True, title=title, addplot=ap)


def draw_filtered(stock_history, save=False, title="Default", save_name="testsave.png"):
    processed_min = As.return_filtered_closing(stock_history)

    df_close_min = pd.DataFrame(index=stock_history.index.tolist(), data=processed_min)

    ap = [mpf.make_addplot(df_close_min, markersize=100)]
    if save:
        mpf.plot(stock_history, type="line", volume=True, addplot=ap, title=title, savefig=save_name)
    else:
        mpf.plot(stock_history, type="line", volume=True, title=title, addplot=ap)


def draw_minmax_on_filtered(stock_history, save=False, title="Default", save_name="testsave.png"):
    [processed_min, processed_max] = As.return_minmax_filtered(stock_history)

    df_close_min = pd.DataFrame(index=stock_history.index.tolist(), data=processed_min)
    df_close_max = pd.DataFrame(index=stock_history.index.tolist(), data=processed_max)

    filtery = As.return_filtered_closing(stock_history)

    df_filtered = pd.DataFrame(index=stock_history.index.tolist(), data=filtery)

    ap = [mpf.make_addplot(df_close_min, type="scatter", markersize=100, marker='^'),
          mpf.make_addplot(df_close_max, type="scatter", markersize=100, marker='v'),
          mpf.make_addplot(df_filtered, markersize=100)]
    if save:
        mpf.plot(stock_history, type="line", volume=True, addplot=ap, title=title, savefig=save_name)
    else:
        mpf.plot(stock_history, type="line", volume=True, title=title, addplot=ap)