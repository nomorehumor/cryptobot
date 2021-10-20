import requests
import json
import time
import datetime
import pandas as pd
import argparse
import os


# log interval in secs
interval = 60

class TradesRetriever():
    
    def __init__(self, tickers, log_dir) -> None:
        columns = ['datetime']
        columns.extend(tickers)
        self.tickers = tickers
        self.df = pd.DataFrame(columns=columns)
        self.df_id = datetime.datetime.now().strftime("%H%M%S_%d%m%Y")
        self.log_dir = log_dir

    def save_df(self, output_dir=None):
        if output_dir is None:
            output_dir = self.log_dir
        self.df.to_csv(os.path.join(output_dir, f"data_{self.df_id}.csv"))

    def get_ticker_fields(self, fields=["last_trade"], df_save=True):
        current_time = datetime.datetime.now().strftime("%H%M%S_%d%m%Y")

        url = "https://api.exmo.com/v1.1/ticker"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = requests.post(url, headers=headers)
        content = json.loads(resp.content)

        all_data = dict()
        new_row = dict()
        new_row["datetime"] = current_time
        for ticker in self.tickers:
            all_data[ticker] = dict()
            for field in fields:

                data = content[ticker][field]

                all_data[ticker][field] = data
                new_row[ticker] = data
        
        self.df = self.df.append(new_row, ignore_index=True)
                
        if df_save:
            self.save_df()

        return all_data



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataframe", default=None,
                        help="Existing dataframe to continue")
    parser.add_argument("--interval", default=60, help="Logging interval")
    parser.add_argument("--tickers", nargs='+',
                        default=["ETH_USD", "BTC_USD"], help="Tickers to track")
    args = parser.parse_args()

    retriever = TradesRetriever(log_dir="data", tickers=args.tickers)

    if args.dataframe:
        retriever.df = pd.read_csv(args.dataframe)

    os.makedirs("data", exist_ok=True)

    running = True
    fields = ["last_trade"]
    while running:
        data = retriever.get_ticker_fields(fields)
        print(data)
        time.sleep(args.interval)
