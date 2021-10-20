import requests
import json
import time
import datetime
import pandas as pd
import argparse
import os

tickers = ["BTC_USD", "ETH_USD"]
fields = ["last_trade"]

# log interval in secs
interval = 60

def get_ticker_fields(tickers, fields=["last_trade"], dataframe=None):
    url = "https://api.exmo.com/v1.1/ticker"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url, headers=headers)
    content = json.loads(resp.content)

    all_data = dict()
    for ticker in tickers:
        all_data[ticker] = dict()
        for field in fields:
            current_time = datetime.datetime.now().strftime("%S%M%H_%d%m%Y")
            
            data = content[ticker][field]
            
            all_data[ticker][field] = data
            if dataframe is not None:
                dataframe = dataframe.append({"datetime": current_time,
                                              "ticker": ticker,
                                              "field": field,
                                              "data": data}, ignore_index=True)
    if dataframe is None:
        return all_data
    else:
        return all_data, dataframe


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataframe", default=None, help="Existing dataframe to continue")
    parser.add_argument("--interval", default=60, help="Logging interval")
    parser.add_argument("--tickers", nargs='+', default=["ETH_USD", "BTC_USD"], help="Tickers to track")
    args = parser.parse_args()
    
    if args.dataframe:
        df = pd.read_csv("data_024716_18102021.csv")
    else:
        df = pd.DataFrame(columns=['datetime', 'ticker', 'field', 'data'])
        
        
    current_time = datetime.datetime.now().strftime("%H%M%S_%d%m%Y")
    os.makedirs("data", exist_ok=True)
    
    running = True
    while running:
        data, df = get_ticker_fields(args.tickers, fields, dataframe=df)
        print(data)
        df.to_csv(os.path.join("data" ,f"data_{current_time}.csv"))
        time.sleep(args.interval)
