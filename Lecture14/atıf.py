import pandas as pd
import numpy as np

INITIAL_CAPITAL = 3000
FEE_RATE = 0.001
ASSETS = ['BTC', 'ADA', 'SOL']

# -----------------------------
# LOAD & TRANSPOSE
# -----------------------------
def load_price_csv(path, asset):
    df = pd.read_csv(path, header=None)
    prices = df.iloc[0].astype(float)   # tek satırı al
    prices = prices.reset_index(drop=True)
    return pd.DataFrame({asset: prices})

btc = load_price_csv("BTCUSDT_price.csv", "BTC")
ada = load_price_csv("ADAUSDT_price.csv", "ADA")
sol = load_price_csv("SOLUSDT_price.csv", "SOL")

# -----------------------------
# ALIGN
# -----------------------------
min_len = min(len(btc), len(ada), len(sol))

df = pd.concat([
    btc.tail(min_len),
    ada.tail(min_len),
    sol.tail(min_len)
], axis=1).reset_index(drop=True)

df = df.tail(1000)

print("FINAL DATA SHAPE:", df.shape)
print(df.head())

# -----------------------------
# BUY & HOLD
# -----------------------------
def buy_and_hold(prices):
    holdings = {a: (INITIAL_CAPITAL / 3) / prices[a].iloc[0] for a in ASSETS}
    return sum(holdings[a] * prices[a].iloc[-1] for a in ASSETS)

# -----------------------------
# REBALANCE
# -----------------------------
def rebalance_backtest(prices, freq):
    holdings = {a: (INITIAL_CAPITAL / 3) / prices[a].iloc[0] for a in ASSETS}
    total_fee = 0

    for t in range(1, len(prices)):
        if t % freq == 0:
            value = sum(holdings[a] * prices[a].iloc[t] for a in ASSETS)
            target = value / 3
            traded = 0

            for a in ASSETS:
                curr = holdings[a] * prices[a].iloc[t]
                diff = target - curr
                traded += abs(diff)
                holdings[a] = target / prices[a].iloc[t]

            fee = traded * FEE_RATE
            total_fee += fee

            for a in ASSETS:
                holdings[a] -= (fee / 3) / prices[a].iloc[t]

    final_value = sum(holdings[a] * prices[a].iloc[-1] for a in ASSETS)
    return final_value, total_fee

# -----------------------------
# RUN
# -----------------------------
bh = buy_and_hold(df)
daily, daily_fee = rebalance_backtest(df, 1)
weekly, weekly_fee = rebalance_backtest(df, 7)
monthly, monthly_fee = rebalance_backtest(df, 30)

results = pd.DataFrame({
    "Strategy": ["Buy & Hold", "Daily", "Weekly", "Monthly"],
    "Final Value (USDT)": [bh, daily, weekly, monthly],
    "Total Fees (USDT)": [0, daily_fee, weekly_fee, monthly_fee]
})

results["Rebalancing Profit vs Buy&Hold"] = results["Final Value (USDT)"] - bh

results
