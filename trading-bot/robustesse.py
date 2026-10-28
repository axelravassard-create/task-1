"""Teste si les bons résultats du backtest résistent : sans 2017, selon le
mois de départ, avec d'autres réglages, sur d'autres cryptos, avec plus de frais.

    python robustesse.py   (quelques minutes)
"""
import itertools, numpy as np, pandas as pd
import strategy as s
from backtest import simulate, stats, ASSETS
from data import coinbase_history

closes = pd.DataFrame({n: coinbase_history(p) for n, p in ASSETS.items()}).sort_index()
start = closes["BTC"].dropna().index[s.MIN_HISTORY]
c = closes.ffill().fillna(1.0)
w = s.target_weights(closes)
bot = simulate(c.loc[start:], w.loc[start:])
btc = closes["BTC"].loc[start:] / closes["BTC"].loc[start]

print("== 1. Sans 2017 (2018-2026) ==")
b2, h2 = bot.loc["2018":], btc.loc["2018":]
print(pd.DataFrame({"Bot": stats(b2), "BTC": stats(h2)}).to_string())

print("\n== 2. Si tu avais commencé n'importe quel mois : résultat après 1, 2, 3 ans ==")
for yrs in (1, 2, 3):
    d = 365 * yrs
    rb = (bot.shift(-d) / bot - 1).dropna().iloc[::30]
    rh = (btc.shift(-d) / btc - 1).dropna().iloc[::30]
    print(f"{yrs} an(s): bot gagnant {(rb>0).mean():.0%} des cas (médiane {rb.median():+.0%}, pire {rb.min():+.0%}) | BTC gagnant {(rh>0).mean():.0%} (médiane {rh.median():+.0%}, pire {rh.min():+.0%})")

print("\n== 3. Autres réglages (pas seulement ceux choisis) ==")
res = []
orig = (s.LOOKBACKS, s.MA_WINDOW, s.REGIME_WINDOW, s.TARGET_VOL)
for lb, ma, rg, tv in itertools.product([(10,40,80),(20,60,120),(30,90,180)], [50,100,150], [150,200,250], [0.3,0.4,0.5]):
    s.LOOKBACKS, s.MA_WINDOW, s.REGIME_WINDOW, s.TARGET_VOL = lb, ma, rg, tv
    b = simulate(c.loc[start:], s.target_weights(closes).loc[start:]).loc["2018":]
    yrs = (b.index[-1]-b.index[0]).days/365
    res.append(((b.iloc[-1]/b.iloc[0])**(1/yrs)-1, (b/b.cummax()-1).min()))
s.LOOKBACKS, s.MA_WINDOW, s.REGIME_WINDOW, s.TARGET_VOL = orig
r = pd.DataFrame(res, columns=["cagr","dd"])
print(f"{len(r)} réglages testés (2018-2026) : rendement annuel min {r.cagr.min():+.0%}, médian {r.cagr.median():+.0%}, max {r.cagr.max():+.0%}; rentables {(r.cagr>0).mean():.0%}; pire chute médiane {r.dd.median():.0%}")

print("\n== 4. Sur des cryptos jamais utilisées pour concevoir le bot ==")
for name in ["LTC-USD","LINK-USD","ADA-USD","XRP-USD","DOGE-USD","AVAX-USD","DOT-USD"]:
    try:
        px = coinbase_history(name, start="2017-01-01")
    except Exception as e:
        print(name, "indispo", e); continue
    df = pd.DataFrame({"BTC": closes["BTC"], "X": px}).sort_index()
    ww = s.target_weights(df)[["X"]]
    st = df["X"].dropna().index[s.MIN_HISTORY]
    b = simulate(df[["X"]].ffill().fillna(1).loc[st:], ww.loc[st:])
    h = df["X"].loc[st:]/df["X"].loc[st]
    yrs=(b.index[-1]-b.index[0]).days/365
    f=lambda x:f"{(x.iloc[-1])**(1/yrs)-1:+.0%}/an, pire {(x/x.cummax()-1).min():.0%}"
    print(f"{name:9} depuis {st.year}: bot {f(b)} | garder {f(h)}")

print("\n== 5. Frais doublés (0,8 % + 0,2 %) ==")
import backtest; backtest.FEE, backtest.SLIPPAGE = 0.008, 0.002
b = backtest.simulate(c.loc[start:], w.loc[start:])
print(stats(b), "| sans 2017:", stats(b.loc["2018":])["Rendement annuel"])
