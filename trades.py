# 2) Paste the backtest script (2-year, $1000, 50/200 MA crossover)
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

ticker = "QBTS"
end = datetime.today()
start = end - timedelta(days=2*365)

df = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
if df.empty:
    raise SystemExit("No data returned for QBTS.")

df["SMA50"] = df["Adj Close"].rolling(50).mean()
df["SMA200"] = df["Adj Close"].rolling(200).mean()

df["prev_diff"] = (df["SMA50"] - df["SMA200"]).shift(1)
df["diff"] = df["SMA50"] - df["SMA200"]
df["Buy"] = (df["prev_diff"] <= 0) & (df["diff"] > 0)
df["Sell"] = (df["prev_diff"] >= 0) & (df["diff"] < 0)

cash, shares = 1000.0, 0.0
for i, row in df.iterrows():
    price = row["Adj Close"]
    if row["Buy"] and cash > 0:
        shares, cash = cash/price, 0.0
    elif row["Sell"] and shares > 0:
        cash, shares = shares*price, 0.0

final_value = cash + shares*df["Adj Close"].iloc[-1]
print(f"Start: $1000.00")
print(f"End:   ${final_value:.2f}")
print(f"Return: {(final_value-1000)/1000*100:.2f}%")
