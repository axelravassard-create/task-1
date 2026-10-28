"""La stratégie : suivi de tendance multi-actifs avec contrôle du risque.

Idée : les cryptos ont des tendances longues et fortes, et des krachs violents
(-70 à -85 %). On est investi quand la tendance est haussière, et on passe en
euros quand elle se retourne. On ne cherche pas le sommet ni le creux : on
cherche à capter le gros du mouvement et à éviter le gros des krachs.

Pour chaque actif, chaque jour :
1. Score de tendance = moyenne de plusieurs signaux simples (rendement sur
   20, 60 et 120 jours positif ? prix au-dessus de sa moyenne 100 jours ?).
   Plusieurs horizons au lieu d'un seul = moins de dépendance à un réglage.
2. Taille de position inversement proportionnelle à la volatilité récente :
   quand le marché s'agite, on réduit.
3. Filtre de régime : si le BTC passe sous sa moyenne 200 jours, tout le
   marché crypto est considéré baissier et on sort de tout (en 2022, ce
   filtre fait passer la pire chute du bot de -70 % à environ -40 %).
4. Plafonds : un actif ne dépasse jamais MAX_PER_ASSET du capital, et le
   total investi ne dépasse jamais 100 % (pas d'effet de levier).
"""
import numpy as np
import pandas as pd

LOOKBACKS = (20, 60, 120)
MA_WINDOW = 100
REGIME_WINDOW = 200   # moyenne longue du BTC pour le filtre de régime
REGIME_ASSET = "BTC"
VOL_WINDOW = 30
TARGET_VOL = 0.40      # volatilité annuelle visée par actif
MAX_PER_ASSET = 0.40   # 40 % du capital au maximum sur un même actif
MIN_HISTORY = max(max(LOOKBACKS), MA_WINDOW, VOL_WINDOW, REGIME_WINDOW) + 1


def trend_score(close: pd.Series) -> pd.Series:
    """Entre 0 (aucun signal haussier) et 1 (tous les signaux haussiers)."""
    signals = [(close / close.shift(n) - 1 > 0).astype(float) for n in LOOKBACKS]
    signals.append((close > close.rolling(MA_WINDOW).mean()).astype(float))
    score = sum(signals) / len(signals)
    return score.where(close.notna())


def target_weights(closes: pd.DataFrame) -> pd.DataFrame:
    """Part du capital à placer sur chaque actif, pour chaque jour.

    Le poids du jour J ne dépend que des cours jusqu'à J inclus : il s'applique
    à partir de J+1 (pas de triche avec le futur).
    """
    daily_vol = np.log(closes).diff().rolling(VOL_WINDOW).std()
    annual_vol = daily_vol * np.sqrt(365)
    scores = closes.apply(trend_score)

    weights = scores * (TARGET_VOL / annual_vol).clip(upper=1.0)
    weights = weights.clip(upper=MAX_PER_ASSET).fillna(0.0)

    btc = closes[REGIME_ASSET]
    bull_market = (btc > btc.rolling(REGIME_WINDOW).mean()).astype(float)
    weights = weights.mul(bull_market, axis=0)

    total = weights.sum(axis=1)
    weights = weights.div(total.where(total > 1.0, 1.0), axis=0)
    return weights
