from datetime import datetime, timedelta
import requests
import pandas as pd
from utils.utils import get_csv_data, save_csv_data


def get_current_price(pair):
    headers = {"Accept": "application/json"}

    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
    response = requests.request("GET", url, headers=headers).json()["result"]
    last_price = next(iter(response.values()))["c"][0]

    return float(last_price)

def get_prices():
    pairs = get_csv_data("pairs")
    
    new_data = {
    }

    df = get_csv_data("historic_data", index_col=0)

    today = datetime.now().strftime('%Y-%m-%d')
    df[today] = float(0)  # Set default value as 0 for today's prices

    for index, row in pairs.iterrows():
        coin= row["Coin"]
        pair = row["Pair"]
        new_data[coin] = get_current_price(pair)

        if coin not in df.index:
            df.loc[coin] = [0] * len(df.columns)

    for coin, price in new_data.items():
        df.at[coin, today] = price


    save_csv_data(df, "historic_data")

def analyze_data():
     df = get_csv_data("historic_data")
     df.columns = pd.to_datetime(df.columns)
     latest_date = df.columns.max()
     one_week_ago = latest_date - timedelta(days=7)

     for coin in df.index:
        current = df.at[coin, latest_date]
        past = df.at[coin, one_week_ago]

        try:
            current = float(current)
            past = float(past)

            change = current - past
            pct_change = (change / past) * 100 if past != 0 else float('inf')

            print(f"{coin}: {past} ➝ {current} | Change: {change:.2f} ({pct_change:.2f}%)")
        except:
            print(f"{coin}: Could not compare (missing or invalid data)")

get_prices()