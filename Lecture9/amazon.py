import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.ar_model import AutoReg

# -------------------------
# 1. Get Data
# -------------------------
ticker = 'AMZN'
amazon = yf.Ticker(ticker)
history = amazon.history(period='500d')

# Use only Close prices
data = history['Close']

# Convert to a proper pandas series
data = data.asfreq('D')   # Daily frequency
data = data.fillna(method='ffill')

# -------------------------
# 2. Train/Test Split
# -------------------------
train = data[:-30]
test = data[-30:]

# -------------------------
# 3. ARMA MODEL (using AutoReg for ARMA-like model)
# -------------------------
arma_model = AutoReg(train, lags=5).fit()
arma_forecast = arma_model.predict(start=len(train), 
                                   end=len(train)+len(test)-1)

# -------------------------
# 4. ARIMA MODEL
# -------------------------
arima_model = ARIMA(train, order=(5,1,2)).fit()
arima_forecast = arima_model.predict(start=len(train),
                                     end=len(train)+len(test)-1)

# -------------------------
# 5. SARIMA MODEL
# -------------------------
sarima_model = SARIMAX(train,
                       order=(5,1,2),
                       seasonal_order=(1,1,1,7)).fit()

sarima_forecast = sarima_model.predict(start=len(train),
                                       end=len(train)+len(test)-1)

# -------------------------
# 6. Plot predictions
# -------------------------
plt.figure(figsize=(12,6))
plt.plot(data.index, data, label="Actual Price")
plt.plot(test.index, arma_forecast, label="ARMA Forecast")
plt.plot(test.index, arima_forecast, label="ARIMA Forecast")
plt.plot(test.index, sarima_forecast, label="SARIMA Forecast")
plt.legend()
plt.title("Amazon Stock Price Prediction")
plt.show()

# -------------------------
# 7. Print future forecast (next 30 days ahead)
# -------------------------
future_days = 30

future_arima = arima_model.predict(len(data), len(data)+future_days-1)
future_sarima = sarima_model.predict(len(data), len(data)+future_days-1)

print("\nARIMA Next 30 Days Forecast:")
print(future_arima)

print("\nSARIMA Next 30 Days Forecast:")
print(future_sarima)
