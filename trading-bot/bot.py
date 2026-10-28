"""Le bot : à lancer une fois par jour, juste après minuit UTC.

    python bot.py            # simulation avec 1 000 € fictifs (par défaut)
    python bot.py --live     # vrai argent sur Kraken (lire le README avant)

À chaque lancement : il télécharge les cours, calcule les poids cibles de la
stratégie, compare avec ce qu'il détient et passe les ordres nécessaires.
"""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from data import kraken_closes
from kraken import Kraken, last_price
from strategy import target_weights

# Actif -> (paire Kraken, code de l'actif dans le solde Kraken)
ASSETS = {"BTC": ("XBTEUR", "XXBT"), "ETH": ("ETHEUR", "XETH"), "SOL": ("SOLEUR", "SOL")}
CASH = "ZEUR"
PAPER_CAPITAL_EUR = 1000  # capital de départ de la simulation
# Plafond optionnel en mode réel. Sans plafond, le bot gère tout le compte et
# réinvestit donc ses gains : c'est ce que suppose le backtest.
MAX_CAPITAL_EUR = float(os.environ.get("MAX_CAPITAL_EUR", "inf"))
REBALANCE_BAND = 0.05   # même seuil que dans le backtest
MIN_ORDER_EUR = 10      # en dessous, un ordre coûte plus qu'il ne rapporte
PAPER_FEE = 0.0040

HERE = Path(__file__).parent
PAPER_STATE = HERE / "paper_state.json"
JOURNAL = HERE / "journal.csv"


def load_paper() -> dict:
    if PAPER_STATE.exists():
        return json.loads(PAPER_STATE.read_text())
    return {"cash": PAPER_CAPITAL_EUR, "holdings": {name: 0.0 for name in ASSETS}}


def log(row: dict):
    pd.DataFrame([row]).to_csv(JOURNAL, mode="a", header=not JOURNAL.exists(), index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="trader avec de l'argent réel")
    parser.add_argument("--dry-run", action="store_true", help="afficher les ordres sans rien exécuter")
    args = parser.parse_args()

    closes = pd.DataFrame({name: kraken_closes(pair) for name, (pair, _) in ASSETS.items()})
    targets = target_weights(closes).iloc[-1]
    price = {name: last_price(pair) for name, (pair, _) in ASSETS.items()}

    if args.live:
        client = Kraken(os.environ["KRAKEN_API_KEY"], os.environ["KRAKEN_API_SECRET"])
        balance = client.balance()
        holdings = {name: balance.get(code, 0.0) for name, (_, code) in ASSETS.items()}
        cash = balance.get(CASH, 0.0)
    else:
        state = load_paper()
        holdings, cash = state["holdings"], state["cash"]

    positions = {name: holdings[name] * price[name] for name in ASSETS}
    equity = min(cash + sum(positions.values()), MAX_CAPITAL_EUR) if args.live else cash + sum(positions.values())
    mode = "RÉEL" if args.live else "SIMULATION"
    print(f"[{mode}] {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC — capital géré : {equity:,.2f} €")

    # Les ventes d'abord, pour libérer les euros des achats.
    orders = []
    for name in ASSETS:
        current = positions[name] / equity if equity else 0.0
        target = float(targets[name])
        gap = target - current
        if abs(gap) <= REBALANCE_BAND and target > 0:
            continue
        if target == 0 and positions[name] < MIN_ORDER_EUR:
            continue
        amount = gap * equity if target > 0 else -positions[name]
        if abs(amount) >= MIN_ORDER_EUR:
            orders.append((name, amount))
    orders.sort(key=lambda o: o[1])

    for name, target in targets.items():
        print(f"  {name}: cible {target:5.0%} | détenu {positions[name] / equity if equity else 0:5.0%}")
    if not orders:
        print("  Aucun ordre aujourd'hui.")

    for name, amount in orders:
        pair = ASSETS[name][0]
        side = "buy" if amount > 0 else "sell"
        volume = min(abs(amount) / price[name], holdings[name]) if side == "sell" else abs(amount) / price[name]
        print(f"  -> {'ACHAT' if side == 'buy' else 'VENTE'} {volume:.6f} {name} (~{abs(amount):,.2f} €)")
        if args.dry_run:
            continue
        if args.live:
            result = client.market_order(pair, side, volume)
            print(f"     ordre envoyé : {result.get('txid')}")
        else:
            if side == "buy":
                volume = min(volume, cash / (1 + PAPER_FEE) / price[name])
                cash -= volume * price[name] * (1 + PAPER_FEE)
                holdings[name] += volume
            else:
                value = volume * price[name]
                cash += value * (1 - PAPER_FEE)
                holdings[name] -= volume
        log({"date": datetime.now(timezone.utc).isoformat(timespec="seconds"), "mode": mode,
             "actif": name, "sens": side, "volume": round(volume, 8), "prix": price[name],
             "montant_eur": round(volume * price[name], 2)})

    if not args.live and not args.dry_run:
        PAPER_STATE.write_text(json.dumps({"cash": cash, "holdings": holdings}, indent=2))
        total = cash + sum(holdings[n] * price[n] for n in ASSETS)
        print(f"  Portefeuille fictif : {total:,.2f} € (départ {PAPER_CAPITAL_EUR:,.0f} €)")


if __name__ == "__main__":
    main()
