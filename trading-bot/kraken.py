"""Client minimal pour l'API privée de Kraken (solde et ordres au marché)."""
import base64
import hashlib
import hmac
import time
import urllib.parse

import requests

API = "https://api.kraken.com"


class Kraken:
    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = base64.b64decode(secret)

    def _private(self, method: str, **data) -> dict:
        path = f"/0/private/{method}"
        data["nonce"] = str(int(time.time() * 1000))
        post = urllib.parse.urlencode(data)
        digest = hashlib.sha256((data["nonce"] + post).encode()).digest()
        signature = hmac.new(self.secret, path.encode() + digest, hashlib.sha512)
        headers = {"API-Key": self.key, "API-Sign": base64.b64encode(signature.digest()).decode()}
        r = requests.post(API + path, data=data, headers=headers, timeout=20)
        r.raise_for_status()
        payload = r.json()
        if payload["error"]:
            raise RuntimeError(f"Kraken {method} : {payload['error']}")
        return payload["result"]

    def balance(self) -> dict[str, float]:
        return {k: float(v) for k, v in self._private("Balance").items()}

    def market_order(self, pair: str, side: str, volume: float) -> dict:
        return self._private("AddOrder", pair=pair, type=side, ordertype="market", volume=f"{volume:.8f}")


def last_price(pair: str) -> float:
    r = requests.get(f"{API}/0/public/Ticker", params={"pair": pair}, timeout=20)
    r.raise_for_status()
    # Kraken peut renommer la paire (XBTEUR -> XXBTZEUR) : on prend l'unique résultat.
    (ticker,) = r.json()["result"].values()
    return float(ticker["c"][0])
