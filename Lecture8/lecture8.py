import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('GOOG.csv')

def create_reg_trading_condition(df):
    # Work on a copy so we don't break the original df unexpectedly
    df = df.copy()

    # Feature columns
    df['Open-Close'] = df['Open'] - df['Close']
    df['High-Low'] = df['High'] - df['Low']

    # Define the target: next day's close - today's close
    df['Target'] = df['Close'].shift(-1) - df['Close']

    # Drop rows with NaNs (from shift etc.)
    df = df.dropna()

    X = df[['Open-Close', 'High-Low']]
    Y = df['Target']

    return df, X, Y

from sklearn.model_selection import train_test_split

df_feat, X, Y = create_reg_trading_condition(df)

# Scatter matrix for the features and target
pd.plotting.scatter_matrix(
    df_feat[['Open-Close', 'High-Low', 'Target']],
    grid=True,
    diagonal='kde'
)
plt.show()

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, shuffle=False, train_size=0.8
)

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

# OLS model
ols = linear_model.LinearRegression()
ols.fit(X_train, Y_train)

print('Coefficients:', ols.coef_)
print('Intercept:', ols.intercept_)

# Train performance
train_predict = ols.predict(X_train)
train_mse = mean_squared_error(Y_train, train_predict)
train_r2 = r2_score(Y_train, train_predict)

print('Train Mean Squared Error:', train_mse)
print('Train R2 Score:', train_r2)

# Test performance
test_predict = ols.predict(X_test)
test_mse = mean_squared_error(Y_test, test_predict)
test_r2 = r2_score(Y_Test, test_predict)

print('Test Mean Squared Error:', test_mse)
print('Test R2 Score:', test_r2)

# ==========================
# Trading logic on df_feat
# ==========================

# Raw prediction (regression output)
df_feat['Predicted_Return'] = ols.predict(X)

# Turn prediction into a trading signal: 1 = long, -1 = short
df_feat['Predicted_Signal'] = np.where(df_feat['Predicted_Return'] > 0, 1, -1)

# Compute log returns
df_feat['GOOG_Returns'] = np.log(df_feat['Close'] / df_feat['Close'].shift(1))
df_feat['GOOG_Returns'] = df_feat['GOOG_Returns'].fillna(0)

# Train/test split index based on X_train length
split_value = len(X_train)

# Strategy returns: use yesterday's signal on today's return
df_feat['Strategy_Returns'] = df_feat['GOOG_Returns'] * df_feat['Predicted_Signal'].shift(1)
df_feat['Strategy_Returns'] = df_feat['Strategy_Returns'].fillna(0)

# Cumulative returns (in %), only on test period
cum_goog_return = df_feat.iloc[split_value:]['GOOG_Returns'].cumsum() * 100
cum_strategy_return = df_feat.iloc[split_value:]['Strategy_Returns'].cumsum() * 100

def plot_chart(cum_symbol_return, cum_strategy_return):
    plt.figure(figsize=(10, 5))
    plt.plot(cum_symbol_return, label='Cum Symbol Return')
    plt.plot(cum_strategy_return, label='Cum Strategy Return')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return (%)')
    plt.title('Buy & Hold vs Strategy')
    plt.show()

plot_chart(cum_goog_return, cum_strategy_return)

# Lasso model for feature selection / comparison
lasso = linear_model.Lasso(alpha=0.001)
lasso.fit(X_train, Y_train)
print('Lasso Coefficients:', lasso.coef_)
