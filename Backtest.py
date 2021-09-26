import yfinance as yf
import pandas as pd
import AnalysisModule as As
import GraphFunctions as Gf
import mplfinance as mpf
import DatabaseStocks as Ds

stock = "GME"
stock_list = Ds.get_smaller_investing_lists()
average_win = 0
plays = 0
old_plays = 0
how_much_time_to_wait = 30

for stock in stock_list:
    try:
        ticker_handle = yf.Ticker(stock)
        history = ticker_handle.history(interval="1d", period="10y", threads=False)
        history.dropna(subset=["Close"], inplace=True)

        days_in_history = len(history.index)
        end_of_prediction_interval = days_in_history - how_much_time_to_wait

        predictionIndex = 150
        while predictionIndex < end_of_prediction_interval:
            #print("**************************************************************")
            prediction_df = history.iloc[predictionIndex-150:predictionIndex, :]
            #print(prediction_df)
            if As.is_cup_and_hadle(prediction_df) and As.sma_potential_buy(prediction_df):
                #Gf.draw_minmax_on_filtered(prediction_df)
                results_df = history.iloc[predictionIndex:predictionIndex+how_much_time_to_wait, :]
                #print("broke out on ", results_df.index[0])
                result_list = [x / results_df['Open'].tolist()[0] for x in results_df['Close'].tolist()]
                print(result_list)
                max_win = 1
                for index, element in enumerate(result_list):
                    if element > max_win:
                        max_win = element
                    if (max_win - element) > 0.05:
                        average_win += element
                        plays += 1
                        break
                    if element > 1.2:
                        average_win += element
                        plays += 1
                        break
                    if index == (len(result_list) - 1):
                        average_win += element
                        plays += 1
                        break
                print("Max up from open", 100*(max(results_df['Close'].tolist()) - results_df['Open'].tolist()[0])/results_df['Open'].tolist()[0])
                #print(results_df)
                #mpf.plot(results_df, type="line", title="results")
                predictionIndex += how_much_time_to_wait * 2
            predictionIndex += 1
    except:
        pass
    if plays != old_plays:
        old_plays = plays
        print(average_win/plays, "out of ", plays, "plays")
