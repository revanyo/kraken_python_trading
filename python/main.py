from datetime import datetime, timedelta
import pandas as pd
from utils.utils import get_csv_data
from kraken.orders import post_market_order

def analyze_data():
     df = get_csv_data("historic_data",index_col=0)
     df.columns = pd.to_datetime(df.columns)
     latest_date = df.columns.max()
     one_week_ago = latest_date - timedelta(days=7)

     for coin in df.index:
        current = df.at[coin, latest_date]
        past = df.at[coin, one_week_ago]
        pairs_df = get_csv_data("pairs",index_col="Coin")
        pair = pairs_df.at[coin, "Pair"]

        try:
            current = float(current)
            past = float(past)

            change = current - past
            pct_change = round(((change / past)*100),2)
            print(f"{pct_change}%")
            if pct_change <= -5:
                post_market_order(pair, 5, "buy")
            if pct_change >= 10:
                post_market_order(pair, 10, "sell")
        except:
            print(f"{coin}: Could not compare (missing or invalid data)")