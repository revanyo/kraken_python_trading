import requests
import uuid
import requests
import time 
from .kraken_auth import handle_kraken_auth
from python.utils.utils import load_dict_file

def get_current_price(pair):
    headers = {"Accept": "application/json"}

    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
    response = requests.request("GET", url, headers=headers).json()["result"]
    last_price = next(iter(response.values()))["c"][0]

    return float(last_price)


def post_market_order(pair, amount, type):
    urlpath = "/0/private/AddOrder"
    api_url = "https://api.kraken.com" + urlpath

    nonce = str(int(time.time() * 1000))

    payload = {
        "nonce": nonce,
        "ordertype": "market",
        "type": type,
        "volume": float(amount/get_current_price(pair)),
        "pair": pair,
        "cl_ord_id": str(uuid.uuid4()).replace("-", "")
        }
    
    api_key, signature = handle_kraken_auth(urlpath, payload)

    headers = {
        "API-Key": api_key,
        "API-Sign": signature,
        "User-Agent": "kraken-api-client"
    }

    response=requests.post(api_url, headers=headers, data=payload).json()
    print(response)

def get_current_balance(coin):
    coin_map = load_dict_file("coin_map")
    coin = coin_map.get(coin.lower())

    urlpath = "/0/private/Balance"

    payload = {
        "nonce": str(int(time.time() * 1000))
    }

    api_key, signature = handle_kraken_auth(urlpath, payload)
    
    api_url = "https://api.kraken.com" + urlpath

    headers = {
        "API-Key": api_key,
        "API-Sign": signature,
        "User-Agent": "kraken-api-client"
    }

    response = requests.post(api_url, headers=headers, data=payload)
    current_balance = response.json()['result'][coin]
    print(current_balance)
    return current_balance

def get_current_balance_in_usd(coin):
    coins = get_current_balance(coin)
    return coins*get_current_price(coin)