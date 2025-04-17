import requests

url = "https://api.kraken.com/0/public/Ticker"

payload = {}
headers = {
  'Accept': 'application/json'
}

data = requests.request("GET", url, headers=headers, data=payload).json()['result']

for asset, asset_data in data.items():
    gain = float(asset_data['c'][0]) - float(asset_data['o'])
    gain_percentage = (gain/float(asset_data['o']))*100
    if gain_percentage >= 5:
        print(asset)
        print(gain_percentage)
        print()
