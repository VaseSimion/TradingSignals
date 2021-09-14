import numpy as np
import tulipy as ti
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# looks for a rise in the mach histogram and a positive zero crossing between the last 2 values
def macd_potential_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 8, 17, 9)  # for buy signals it should be 8,17,9

    if macdhistogram[-1] > 0 > macdhistogram[-2] and \
            macdhistogram[-1] >= macdhistogram[-2] >= macdhistogram[-3] >= macdhistogram[-4]:
        return True
    else:
        return False


def sma_potential_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    sma = ti.sma(numpyclose, 17)
    if sma[-50] < sma[-5] < sma[-1] < closing_price_list[-1] and closing_price_list[-2] < sma[-2]:
        return True
    else:
        return False


# checks if today is a positive value
def is_today_rising(stock):
    current_value = stock['Close'].tolist()[-1]
    open_value = stock['Open'].tolist()[-1]
    if current_value >= open_value:
        return True
    else:
        return False


# checks if today is a negative value
def is_today_falling(stock):
    current_value = stock['Close'].tolist()[-1]
    open_value = stock['Open'].tolist()[-1]
    if current_value <= open_value:
        return True
    else:
        return False


# checks if the last sma is bigger than the one before it and also that the last two lows are in ascending value
def is_stock_uptrend(stock):
    [minimlist, maximlist] = return_last_minimums_maximum_sell(stock)
    if minimlist[0] > minimlist[1] > minimlist[2] and maximlist[0] > maximlist[1]:
        return True
    else:
        return False


# returns open close values of last day in stock
def return_open_close(stock):
    current_value = stock['Close'].tolist()[-1]
    open_value = stock['Open'].tolist()[-1]
    return [open_value, current_value]


# returns open close values of first day in stock
def return_open_close_first_day(stock):
    current_value = stock['Close'].tolist()[0]
    open_value = stock['Open'].tolist()[0]
    return [open_value, current_value]


def return_last_minimums_maximum_sell(stock):
    processed_min = [float("nan"), float("nan")]
    processed_max = [float("nan"), float("nan")]
    last_found = ("none", 0)
    last_value = 0
    close_list = stock["Close"]

    for index, element in enumerate(close_list[2:-2]):
        if (close_list[index + 1] > element < close_list[index + 3]) and (
                close_list[index] > element < close_list[index + 4]) \
                and (abs((element - last_value) / element) > 0.03):
            processed_min += [element]
            last_value = element
            if last_found[0] == "min":
                processed_min[last_found[1] + 2] = float("nan")
                last_found = ("min", index)
            else:
                last_found = ("min", index)
        else:
            processed_min += [float("nan")]

        if (close_list[index + 1] < element > close_list[index + 3]) and (
                close_list[index] < element > close_list[index + 4]) \
                and (abs((element - last_value) / element) > 0.03):
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

    return [processed_min, processed_max]