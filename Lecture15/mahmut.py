import pandas as pd

btceur = pd.read_csv("BTCEUR_price.csv", header=None)
eurusdt = pd.read_csv("EURUSDT_price.csv", header=None)
btcusdt = pd.read_csv("BTCUSDT_price.csv", header=None)

capital = 1 #btc

margin = 1.0004

for i in range(1000):
    x = btceur.iloc[0,i]
    y = btcusdt.iloc[0,i]
    z = eurusdt.iloc[0,i]
    ratio = (x * z) / y #burası çok önemli, asıl olay burda.

    if ratio > margin:
        print(f"Arbitrage opportunity at index {i}:")
        capital = float(capital)*ratio
        print(f"New capital: {capital} BTC")

percent = 100*capital-100        
print("profit percentage:", percent)