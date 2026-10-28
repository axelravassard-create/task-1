"""Récupération des prix journaliers (bougies) depuis des API publiques, sans clé.

- Historique long pour le backtest : Coinbase (en USD, depuis 2015).
- Données récentes pour le bot : Kraken (en EUR, la plateforme où il trade).
"""
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

CACHE_DIR = Path(__file__).parent / "cache"
DAY = 86400


def coinbase_history(product: str, start: str = "2016-01-01") -> pd.Series:
    """Cours de clôture journaliers de `product` (ex. "BTC-USD"), mis en cache."""
    CACHE_DIR.mkdir(exist_ok=True)
    cache = CACHE_DIR / f"{product}.csv"
    if cache.exists() and time.time() - cache.stat().st_mtime < DAY:
        return pd.read_csv(cache, index_col=0, parse_dates=True)["close"]

    rows = []
    end = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    first = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    while end > first:
        begin = max(first, end - timedelta(days=299))
        r = requests.get(
            f"https://api.exchange.coinbase.com/products/{product}/candles",
            params={"granularity": DAY, "start": begin.isoformat(), "end": end.isoformat()},
            timeout=20,
        )
        r.raise_for_status()
        batch = r.json()
        rows += batch
        end = begin - timedelta(days=1)
        time.sleep(0.25)  # reste poli avec l'API publique

    df = pd.DataFrame(rows, columns=["time", "low", "high", "open", "close", "volume"])
    df["date"] = pd.to_datetime(df["time"], unit="s")
    df = df.drop_duplicates("date").set_index("date").sort_index()
    # La bougie du jour n'est pas terminée : on ne la garde pas.
    df = df[df.index < pd.Timestamp.now(tz="UTC").normalize().tz_localize(None)]
    df[["close"]].to_csv(cache)
    return df["close"]


def kraken_closes(pair: str) -> pd.Series:
    """720 derniers cours de clôture journaliers de `pair` sur Kraken (ex. "XBTEUR")."""
    r = requests.get(
        "https://api.kraken.com/0/public/OHLC",
        params={"pair": pair, "interval": 1440},
        timeout=20,
    )
    r.raise_for_status()
    payload = r.json()
    if payload["error"]:
        raise RuntimeError(f"Kraken : {payload['error']}")
    key = next(k for k in payload["result"] if k != "last")
    df = pd.DataFrame(
        payload["result"][key],
        columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"],
    )
    df["date"] = pd.to_datetime(df["time"], unit="s")
    closes = df.set_index("date")["close"].astype(float)
    return closes.iloc[:-1]  # la dernière bougie est encore en cours
