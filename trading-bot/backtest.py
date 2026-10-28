"""Teste la stratégie sur l'historique, frais compris, et la compare au
simple achat-conservation (« buy & hold »).

    python backtest.py
"""
import numpy as np
import pandas as pd

from data import coinbase_history
from strategy import MIN_HISTORY, target_weights

ASSETS = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD"}
FEE = 0.0040          # frais "taker" Kraken Pro pour un petit compte
SLIPPAGE = 0.0010     # écart entre le prix vu et le prix obtenu
REBALANCE_BAND = 0.05  # on ne bouge un actif que si l'écart dépasse 5 points


def simulate(closes: pd.DataFrame, weights: pd.DataFrame) -> pd.Series:
    """Valeur du portefeuille jour après jour, en partant de 1."""
    returns = closes.pct_change().fillna(0.0)
    held = pd.Series(0.0, index=closes.columns)
    equity, curve = 1.0, []
    for day in closes.index:
        # 1. Le marché bouge avec ce qu'on détient depuis la veille.
        growth = held * (1 + returns.loc[day])
        equity *= 1 + (growth.sum() - held.sum())
        held = growth / (1 + (growth.sum() - held.sum()))
        # 2. En clôture, on rééquilibre vers les poids cibles.
        target = weights.loc[day]
        trade = (target - held).where((target - held).abs() > REBALANCE_BAND, 0.0)
        trade = trade.where(target > 0, -held)  # sortie complète si signal à zéro
        equity *= 1 - trade.abs().sum() * (FEE + SLIPPAGE)
        held = held + trade
        curve.append(equity)
    return pd.Series(curve, index=closes.index)


def stats(curve: pd.Series) -> dict:
    years = (curve.index[-1] - curve.index[0]).days / 365
    daily = curve.pct_change().dropna()
    return {
        "Multiplié par": f"x{curve.iloc[-1] / curve.iloc[0]:.1f}",
        "Rendement annuel": f"{(curve.iloc[-1] / curve.iloc[0]) ** (1 / years) - 1:+.0%}",
        "Pire chute (max drawdown)": f"{(curve / curve.cummax() - 1).min():.0%}",
        "Sharpe": f"{daily.mean() / daily.std() * np.sqrt(365):.2f}",
    }


def yearly_returns(curve: pd.Series) -> pd.Series:
    ends = pd.concat([curve.iloc[:1], curve.resample("YE").last()])
    return ends.pct_change().iloc[1:]


def main():
    closes = pd.DataFrame({name: coinbase_history(p) for name, p in ASSETS.items()}).sort_index()
    weights = target_weights(closes)
    start = closes["BTC"].dropna().index[MIN_HISTORY]
    closes, weights = closes.loc[start:], weights.loc[start:]

    # Avant sa cotation, un actif a un poids nul : son prix fictif n'a pas d'effet.
    bot = simulate(closes.ffill().fillna(1.0), weights)
    hold_btc = closes["BTC"] / closes["BTC"].iloc[0]

    print(f"Période : {start.date()} -> {closes.index[-1].date()}\n")
    table = pd.DataFrame({"Bot (tendance)": stats(bot), "Garder du BTC": stats(hold_btc)})
    print(table.to_string(), "\n")

    print("Par année :")
    yearly = pd.DataFrame({
        "Bot": yearly_returns(bot),
        "BTC": yearly_returns(hold_btc),
    })
    yearly.index = yearly.index.year
    print(yearly.map(lambda x: f"{x:+.0%}").to_string(), "\n")
    print(f"Exposition moyenne : {weights.sum(axis=1).mean():.0%} du capital")


if __name__ == "__main__":
    main()
