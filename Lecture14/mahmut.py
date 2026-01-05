import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

price_btc = pd.read_csv("BTCUSDT_price.csv",)
price_ada = pd.read_csv("ADAUSDT_price.csv",)
price_sol = pd.read_csv("SOLUSDT_price.csv",)

price_btc = price_btc.np.transpose(price_btc)
price_ada = price_ada.np.transpose(price_ada)
price_sol = price_sol.np.transpose(price_sol)

price_btc = price_btc.iloc[:,0]
price_ada = price_ada.iloc[:,0]
price_sol = price_sol.iloc[:,0]

min_len = min(len(price_btc), len(price_ada), len(price_sol))

price_btc = price_btc/price_btc[:,0]
price_ada = price_ada/price_ada[:,0]
price_sol = price_sol/price_sol[:,0]

plt.figure(figsize=(12, 6))
plt.plot(price_btc,label='BTCUSDT')
plt.plot(price_ada,label='ADAUSDT')
plt.plot(price_sol,label='SOLUSDT')
plt.legend()

prices = np.column_stack((price_btc, price_ada, price_sol))
amounts = np.array([1000, 1000, 1000])

com_rate = 0.001
m, n = prices.shape
 
for i in range(m):
    values = prices[i] * amounts 
    average = np.mean(values)
    if i % 7 == 0:
        if np.max(values) > average * (1+com_rate) or np.min(values) < average * (1 - com_rate):
            for k in range(n):
                if values[k] > average:
                    difference = values[k] - average 
                    

