from statsmodels.tsa.arima_model import ARMA
import matplotlib.pyplot as plt
import pandas as pd

# Forecast the first MA(1) model
data = pd.read_csv("data_192934_19102021.csv")
data = data[data["ticker"] == "ETH_USD"]["data"]

data.dropna(inplace=True)


data_dm = data.diff()
data_dm.dropna(inplace=True)

data_dm2 = data_dm.diff()
data_dm2.dropna(inplace=True)

# Plot
fig, axs = plt.subplots(3)
axs[0].plot(data)
axs[1].plot(data_dm)
axs[2].plot(data_dm2)
plt.show()

print(f"got data for {len(data_dm2)} timepoints")
model = ARMA(data_dm2, order=(1,1))
res = model.fit()
res.plot_predict(start=0, end=len(data_dm2) + 100)

# model2 = ARMA(data_dm2, order=(0,1))
# res2 = model2.fit()
# res2.plot_predict(start=len(data_dm2) - 10, end=len(data_dm2) + 10)
plt.show()