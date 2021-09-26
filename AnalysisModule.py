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
    if sma[-50] < sma[-5] < sma[-1] < closing_price_list[-1]:
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


def return_filtered_closing(stock):
    close_list = stock["Close"]
    processed = [close_list[0], close_list[1]]
    for index, element in enumerate(close_list[2:-2]):
        processed.append(sum(close_list[index:index+5])/5)
    processed.append(close_list[-2])
    processed.append(close_list[-1])

    return processed


def return_minmax_filtered(stock):
    processed_min = [float("nan"), float("nan")]
    processed_max = [float("nan"), float("nan")]
    last_found = ("none", 0)
    last_value = 1
    close_list = return_filtered_closing(stock)

    for index, element in enumerate(close_list[2:-2]):
        if (close_list[index + 1] > element < close_list[index + 3]) and\
           (close_list[index] > element < close_list[index + 4]) and \
           ((0.98 > element/last_value) or (1.02 < element/last_value)):
            # print(element, last_value)
            processed_min += [element]
            last_value = element
            if last_found[0] == "min":
                processed_min[last_found[1] + 2] = float("nan")
                last_found = ("min", index)
            else:
                last_found = ("min", index)
        else:
            processed_min += [float("nan")]

        if (close_list[index + 1] < element > close_list[index + 3]) and \
           (close_list[index] < element > close_list[index + 4]) and \
           ((0.98 > element / last_value) or (1.02 < element / last_value)):
            # print(element, last_value)
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
    # print(close_list[-30:])
    # print(processed_max[-30:])
    return [processed_min, processed_max]


# checks if the last sma is bigger than the one before it and also that the last two lows are in ascending value
def is_breaking_out_of_base(stock):
    [raw_minimlist, raw_maximlist] = return_minmax_filtered(stock)
    minimlist = [x for x in raw_minimlist if str(x) != "nan"]
    maximlist = [x for x in raw_maximlist if str(x) != "nan"]
    absolute_min = min(minimlist[-3:])
    absolute_max = max(maximlist[-3:])

    average_min = sum(minimlist[-3:])/3
    average_max = sum(maximlist[-3:])/3
# print(average_min, absolute_min)
    if (absolute_max-absolute_min)/absolute_min < 0.2 and abs((absolute_max-average_max)/absolute_max) < 0.02 and \
            abs((absolute_min-average_min)/absolute_min) < 0.02:
        if stock['Close'].tolist()[-1] > absolute_max:
            return True
        else:
            # print("channel without break")
            return False
    else:
        return False


# checks if the last sma is bigger than the one before it and also that the last two lows are in ascending value
def is_stock_uptrend(stock):
    [raw_minimlist, raw_maximlist] = return_last_minimums_maximum_sell(stock)
    minimlist = [x for x in raw_minimlist if str(x) != "nan"]
    maximlist = [x for x in raw_maximlist if str(x) != "nan"]
    last_min_index = raw_minimlist.index(minimlist[-1]), "out of", len(raw_minimlist)
    last_max_index = raw_maximlist.index(maximlist[-1]), "out of", len(raw_maximlist)
    if last_min_index > last_max_index:
        if stock['Close'].tolist()[-1] > minimlist[-1] > minimlist[-2] > minimlist[-3] \
                and maximlist[-1] > maximlist[-2]:
            return True
        else:
            return False
    else:
        if stock['Close'].tolist()[-1] > minimlist[-1] > minimlist[-2] and \
                maximlist[-1] > maximlist[-2] > maximlist[-3]:
            return True
        else:
            return False


def is_cup_and_hadle(stock):
    [raw_minimlist, raw_maximlist] = return_minmax_filtered(stock)
    minimlist = [x for x in raw_minimlist if str(x) != "nan"]
    maximlist = [x for x in raw_maximlist if str(x) != "nan"]
    last_min_index = raw_minimlist.index(minimlist[-1]), "out of", len(raw_minimlist)
    last_max_index = raw_maximlist.index(maximlist[-1]), "out of", len(raw_maximlist)

    #if stock['Close'].tolist()[-1] < maximlist[-1]:
    #    return False

    if (maximlist[-1]/maximlist[-3]) > 0.9 and (maximlist[-3]/maximlist[-1]) > 0.9:
        if last_min_index > last_max_index:
            maxim_value = min(maximlist[-1], maximlist[-3])
            minim_value = min(minimlist[-2], minimlist[-3])
        else:
            maxim_value = min(maximlist[-1], maximlist[-3])
            minim_value = min(minimlist[-2], minimlist[-1])
        if (maxim_value / minim_value) < 0.8 or (minim_value / maxim_value) < 0.8:
            return True
        else:
            return False
    if (maximlist[-1]/maximlist[-2]) > 0.9 and (maximlist[-2]/maximlist[-1]) > 0.9 and \
            (last_max_index[-1] - last_max_index[-2] > 30):
        if last_min_index > last_max_index:
            maxim_value = min(maximlist[-1], maximlist[-2])
            minim_value = minimlist[-2]
        else:
            maxim_value = min(maximlist[-1], maximlist[-2])
            minim_value = minimlist[-1]
        if (maxim_value / minim_value) < 0.8 or (minim_value / maxim_value) < 0.8:
            return True
        else:
            return False
    return False
