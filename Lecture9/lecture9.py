import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

quotes = pd.read_csv('IBM.csv')
data = quotes[['Date', 'Close']]

data.index = pd.to_datetime(data['Date'], format = 'mixed')

del data ['Date']
all_s = data.describe()

print(all_s)

import seaborn as sns
sns.set()

plt.plot(data.index, data['Close'])
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(rotation=45)
#plt.show()

train = data[data.index < pd.to_datetime('2023-04-10', format = 'mixed')]
test = data[data.index > pd.to_datetime('2023-04-10', format = 'mixed')]

plt.plot(train, color= 'black')
plt.plot(test, color = 'red')
plt.show()

from statsmodels.tsa.statespace.sarimax import SARIMAX

X = train['Close']
ArmaModel = SARIMAX(X, order = (1,0,1))
ArmaModel = ArmaModel.fit()

y_pred = ArmaModel.get_forecast(len(test.index))
y_pred_df = y_pred.conf_int(alpha = 0.05)

y_pred_df['Predictions'] = ArmaModel.predict(start=y_pred_df.index[0], end = y_pred_df.index[-1])

y_pred_df.index = test.index

y_pred_out = y_pred_df['Predictions']

plt.plot(y_pred_out, color = 'green', label = 'Arma Forecasting')
plt.show()

from sklearn.metrics import mean_squared_error 
arma_rmse = np.sqrt(mean_squared_error(test['Close'], y_pred_df['Predictions']))

print(arma_rmse)

SarimaxModel = SARIMAX(X, order=(5, 3, 2), seasonal_order = (2,2,3,6))
SarimaxModel = SarimaxModel.fit()
