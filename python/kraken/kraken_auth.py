import os
import time
import urllib.parse
import hashlib
import hmac
import base64
from dotenv import load_dotenv

def get_kraken_signature(urlpath, data, secret):
    post_data = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + post_data).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def handle_kraken_auth(urlpath):
    if os.getenv("CI") != "true":
        load_dotenv()
    api_key = os.getenv("KRAKEN_API_KEY")
    api_sec = os.getenv("KRAKEN_API_SECRET")
    nonce = str(int(time.time() * 1000))

    payload = {
        "nonce": nonce
    }
    signature = get_kraken_signature(urlpath, payload, api_sec)
    return api_key, payload, signature