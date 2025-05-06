from datetime import datetime
from utils.utils import get_csv_data, save_csv_data
from kraken.kraken_functions import get_current_price

def get_prices():
    pairs = get_csv_data("pairs")
    
    new_data = {
    }

    df = get_csv_data("historic_data", index_col=0)

    today = datetime.now().strftime('%Y-%m-%d')
    df[today] = float(0)

    for index, row in pairs.iterrows():
        coin= row["Coin"]
        pair = row["Pair"]
        new_data[coin] = get_current_price(pair)

        if coin not in df.index:
            df.loc[coin] = [0] * len(df.columns)

    for coin, price in new_data.items():
        df.at[coin, today] = price

    save_csv_data(df, "historic_data")

get_prices()