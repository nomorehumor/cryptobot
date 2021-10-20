import os
import datetime
import pandas as pd
import time

from analyze import forecast_arma_next_n, get_current_trend
from trades import TradesRetriever

portfolio = dict({"USDT": 100.0})
trade_portion = 0.3 # in percent

use_retriever = False 

def main():
    if use_retriever:
        tickers = ["BTC_USD", "ETH_USD"]
        retriever = TradesRetriever(tickers=tickers, log_dir="data")
        
    decision_interval = 60 # in secs
    while True:
        if use_retriever:
            data = retriever.get_ticker_fields()
            df = retriever.df
            print("Current price for BTC_USD", data["BTC_USD"]["last_trade"])
        else:
            df = pd.read_csv("data/data_124852_20102021.csv")
        
        if len(df) > 20:
            btc_df = df["BTC_USD"]
            current_trends = get_current_trend(btc_df)
            forecast = forecast_arma_next_n(btc_df, 5)
            print("Trends:", current_trends)
            print("Forecast for next values:", forecast)
        else:
            print(f"Not enough data for prediction, retrying in {decision_interval} secs...")
    
        time.sleep(decision_interval)        
        
if __name__ == "__main__":
    main()