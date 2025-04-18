import yfinance as yf
import pandas as pd

ticker = "BTC-USD"
df = yf.download(ticker, start="2020-01-01", end="2024-12-31", auto_adjust=True)

drop_threshold = -0.05
gain_threshold = 0.1
buy_amount = 5     # Buy $5 worth on dip
sell_amount = 10   # Sell $10 worth on pump

positions = []
holding_shares = 0
avg_buy_price = 0  # Tracks the average buy price

for i in range(1, len(df)):
    curr_close = float(df.iloc[i]['Close'])
    prev_close = float(df.iloc[i - 1]['Close'])

    # Check for dip
    pct_drop = curr_close / prev_close - 1
    if pct_drop <= drop_threshold:
        shares_bought = buy_amount / curr_close
        total_cost = avg_buy_price * holding_shares + buy_amount
        holding_shares += shares_bought
        avg_buy_price = total_cost / holding_shares  # Recalculate average buy price

    # Check for pump
    if holding_shares > 0 and curr_close >= avg_buy_price * (1 + gain_threshold):
        value_to_sell = min(sell_amount, holding_shares * curr_close)
        shares_to_sell = value_to_sell / curr_close

        profit = shares_to_sell * (curr_close - avg_buy_price)
        positions.append({
            'Date': df.index[i],
            'Sell Price': curr_close,
            'Shares Sold': shares_to_sell,
            'Proceeds': value_to_sell,
            'Profit': profit
        })

        holding_shares -= shares_to_sell
        if holding_shares == 0:
            avg_buy_price = 0  # Reset if fully sold out

trades = pd.DataFrame(positions)
print(trades)
print(f"\nTotal Sells: {len(trades)}")
print(f"Total Profit: ${trades['Profit'].sum():.2f}")
print(f"Remaining Shares: {holding_shares:.6f}")
print(f"Value of Remaining Shares: ${holding_shares * curr_close:.2f}")
