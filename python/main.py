from datetime import datetime
import requests
import pandas as pd


def get_current_price(pair):
    headers = {"Accept": "application/json"}

    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
    response = requests.request("GET", url, headers=headers).json()["result"]
    last_price = next(iter(response.values()))["c"][0]

    return float(last_price)

def get_prices():
    pairs = pd.read_csv("../pairs.csv", names=["coin","pair"])
    
    new_data = {
    }

    df = pd.read_csv("../historic_data.csv", index_col=0)

    today = datetime.now().strftime('%Y-%m-%d')
    df[today] = float(0)  # Set default value as 0 for today's prices

    for index, row in pairs.iterrows():
        coin= row["coin"]
        pair = row["pair"]
        new_data[coin] = get_current_price(pair)

        if coin not in df.index:
            df.loc[coin] = [0] * len(df.columns)

    for coin, price in new_data.items():
        df.at[coin, today] = price


    df.to_csv("../historic_data.csv")


