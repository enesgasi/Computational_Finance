import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

price_btc = pd.read_csv("BTCUSDT_price.csv", header=None)
price_ada = pd.read_csv("ADAUSDT_price.csv", header=None)
price_sol = pd.read_csv("SOLUSDT_price.csv", header=None)

price_btc = price_btc.T
price_ada = price_ada.T
price_sol = price_sol.T

price_btc = price_btc.iloc[:, 0]
price_ada = price_ada.iloc[:, 0]
price_sol = price_sol.iloc[:, 0]

min_len = min(len(price_btc), len(price_ada), len(price_sol))
price_btc = price_btc[:min_len]
price_ada = price_ada[:min_len]
price_sol = price_sol[:min_len]

price_btc_norm = price_btc / price_btc.iloc[0]
price_ada_norm = price_ada / price_ada.iloc[0]
price_sol_norm = price_sol / price_sol.iloc[0]

plt.figure(figsize=(12, 6))
plt.plot(price_btc_norm, label='BTCUSDT')
plt.plot(price_ada_norm, label='ADAUSDT')
plt.plot(price_sol_norm, label='SOLUSDT')
plt.legend()
plt.show()

prices = np.column_stack((price_btc.values, price_ada.values, price_sol.values))

# Her varlığa 1000$ yatırım
initial_value = 1000
amounts = np.array([
    initial_value / prices[0, 0],
    initial_value / prices[0, 1],
    initial_value / prices[0, 2]
])

com_rate = 0.001
m, n = prices.shape
 
for i in range(m):
    values = prices[i] * amounts 
    average = np.mean(values)
    
    if i % 7 == 0:
        if np.max(values) > average * (1 + com_rate) or np.min(values) < average * (1 - com_rate):
            for k in range(n):
                if values[k] > average:
                    difference = values[k] - average 
                    amounts[k] = amounts[k] - (difference * (1 + com_rate)) / prices[i, k]
                else:
                    difference = average - values[k]
                    amounts[k] = amounts[k] + (difference * (1 - com_rate)) / prices[i, k]

final_values = prices[-1] * amounts
final_total = np.sum(final_values)
initial_total = 3 * initial_value

profit_pct = ((final_total - initial_total) / initial_total) * 100

print("Final value:", final_total)
print("Profit percentage:", profit_pct)

