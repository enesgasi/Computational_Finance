import pandas as pd

# Load CSV files (single-row, horizontal prices)
btceur = pd.read_csv("BTCEUR_price.csv", header=None).T
eurusdt = pd.read_csv("EURUSDT_price.csv", header=None).T
btcusdt = pd.read_csv("BTCUSDT_price.csv", header=None).T

# Rename columns
btceur.columns = ["btceur"]
eurusdt.columns = ["eurusdt"]
btcusdt.columns = ["btcusdt"]

# Combine
df = pd.concat([btceur, eurusdt, btcusdt], axis=1)

# Initial capital
btc_balance = 1.0
threshold = 1.0004  # 0.04%

trade_count = 0

# Loop through historical data
for _, row in df.iterrows():
    btc_end = (btc_balance * row["btceur"] * row["eurusdt"]) / row["btcusdt"]

    if btc_end >= btc_balance * threshold:
        btc_balance = btc_end
        trade_count += 1

# Cumulative profit
cumulative_profit_pct = (btc_balance - 1) * 100

print(f"Executed trades: {trade_count}")
print(f"Final BTC balance: {btc_balance:.6f}")
print(f"Cumulative profit (%): {cumulative_profit_pct:.3f}")
