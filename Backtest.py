import yfinance as yf
import pandas as pd
import AnalysisModule as As
import GraphFunctions as Gf
import mplfinance as mpf
import DatabaseStocks as Ds

stock = "GME"
stock_list = Ds.get_smaller_investing_lists()
at_least_5_percent = 0
at_least_10_percent = 0
total_guesses = 0

for stock in stock_list:
    try:
        ticker_handle = yf.Ticker(stock)
        history = ticker_handle.history(interval="1d", period="10y", threads=False)
        history.dropna(subset=["Close"], inplace=True)

        days_in_history = len(history.index)
        end_of_prediction_interval = days_in_history - 30

        predictionIndex = 150
        while predictionIndex < end_of_prediction_interval:
            #print("**************************************************************")
            prediction_df = history.iloc[predictionIndex-150:predictionIndex, :]
            #print(prediction_df)
            if As.is_breaking_out_of_base(prediction_df) and As.sma_potential_buy(prediction_df):
                total_guesses += 1
                #Gf.draw_minmax(prediction_df)
                results_df = history.iloc[predictionIndex:predictionIndex+30, :]
                #print("broke out on ", results_df.index[0])
                if 100*(max(results_df['Close'].tolist()) - results_df['Open'].tolist()[0])/results_df['Open'].tolist()[0] > 5:
                    at_least_5_percent += 1

                if 100*(max(results_df['Close'].tolist()) - results_df['Open'].tolist()[0])/results_df['Open'].tolist()[0] > 10:
                    at_least_10_percent += 1
                #print(results_df)
                #mpf.plot(results_df, type="line", title="results")
                predictionIndex += 30
            predictionIndex += 1
    except:
        pass
    print(at_least_5_percent, "out of", total_guesses, "were right until now for the 5% section")
    print(at_least_10_percent, "out of", total_guesses, "were right until now for the 10% section")