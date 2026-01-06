import pandas as pd

# Load CSV files
btceur = pd.read_csv("BTCEUR_price.csv", header=None)
eurusdt = pd.read_csv("EURUSDT_price.csv", header=None)
btcusdt = pd.read_csv("BTCUSDT_price.csv", header=None)

# Transpose (prices are stored horizontally)
btceur = btceur.T
eurusdt = eurusdt.T
btcusdt = btcusdt.T

# Rename columns
btceur.columns = ["btceur"]
eurusdt.columns = ["eurusdt"]
btcusdt.columns = ["btcusdt"]

# Combine into one DataFrame (aligned by index)
df = pd.concat([btceur, eurusdt, btcusdt], axis=1)

# Initial BTC
df["btc_start"] = 1.0

# Triangular arbitrage calculation
df["eur"] = df["btc_start"] * df["btceur"]
df["usdt"] = df["eur"] * df["eurusdt"]
df["btc_end"] = df["usdt"] / df["btcusdt"]

# Profit percentage
df["profit_pct"] = (df["btc_end"] - 1) * 100

# Arbitrage condition (>= 0.04%)
arb = df[df["profit_pct"] >= 0.04]

# Results
print("Total arbitrage opportunities:", len(arb))
print(arb[["btc_end", "profit_pct"]])

