from statsmodels.tsa.arima_model import ARMA
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_current_trend(ticker_df: pd.DataFrame, trend_lengths=[2, 5, 10, 20, 60]):
    results = list()
    for trend in trend_lengths:
        Y = ticker_df[-trend:]
        time = np.linspace(0, len(Y) - 1, len(Y))
        X = sm.add_constant(time)
        model = sm.OLS(Y, X)
        res = model.fit()
        
        results.append({"trend_length": trend,
                        "R2": res.rsquared, 
                        "param": res.params.x1})
        
    return results
    

def forecast_arma_next_n(ticker_df: pd.DataFrame, n: int):
    ticker_df.dropna(inplace=True)
    df_dm = ticker_df.diff()
    df_dm.dropna(inplace=True)
    df_dm2 = df_dm.diff()
    df_dm2.dropna(inplace=True)

    model = ARMA(df_dm2, order=(1,1))
    res = model.fit()
    return res.predict(start=len(df_dm2) - 1, end=len(ticker_df) + n - 1)    

# # Forecast the first MA(1) model
# data = pd.read_csv("data_192934_19102021.csv")
# data = data[data["ticker"] == "ETH_USD"]["data"]
# data.dropna(inplace=True)

# data_dm = data.diff()
# data_dm.dropna(inplace=True)

# data_dm2 = data_dm.diff()
# data_dm2.dropna(inplace=True)

# # Plot
# fig, axs = plt.subplots(3)
# axs[0].plot(data)
# axs[1].plot(data_dm)
# axs[2].plot(data_dm2)
# plt.show()

# print(f"got data for {len(data_dm2)} timepoints")
# model = ARMA(data_dm2, order=(1,1))
# res = model.fit()
# res.plot_predict(start=0, end=len(data_dm2) + 100)

# plt.show()