# Bot de trading crypto : suivi de tendance

Un bot qui investit sur le **Bitcoin, l'Ethereum et le Solana** quand leur
tendance est haussière, et qui repasse en **euros** quand elle se retourne.
Il décide une fois par jour : pas besoin d'aller vite, ni de surveiller un écran.

## Pourquoi ces choix

| Choix | Raison |
|---|---|
| **Crypto** plutôt qu'actions ou forex | Marché ouvert 24 h/24, API gratuites, petites sommes possibles, et de très fortes tendances : c'est là que le suivi de tendance marche le mieux. |
| **Kraken** comme plateforme | Plateforme ancienne et agréée en Europe, dépôts en euros par virement SEPA, API complète. Binance n'est pas accessible depuis ce serveur. |
| **Suivi de tendance** plutôt que vitesse | Un particulier ne peut pas battre les pros sur la vitesse. Le suivi de tendance est l'une des rares stratégies dont les résultats sont documentés depuis des décennies. |
| **Une décision par jour** | Moins de frais, moins de faux signaux, et le bot peut tourner sur n'importe quel ordinateur. |

## La stratégie en 4 règles

1. **Tendance** : pour chaque crypto, 4 signaux. La hausse sur 20, 60 et 120 jours, et un prix au-dessus de la moyenne 100 jours. Plus il y a de signaux positifs, plus on investit.
2. **Volatilité** : quand le marché s'agite, la position est réduite.
3. **Régime de marché** : si le BTC passe sous sa moyenne 200 jours, le bot vend tout et attend en euros.
4. **Plafonds** : au maximum 40 % du capital sur une même crypto, jamais plus de 100 % au total, aucun effet de levier.

## Résultats sur l'historique (backtest, juillet 2016 à octobre 2026)

Les frais (0,40 %) et le glissement de prix (0,10 %) sont inclus.

|                    | Bot      | Garder du BTC |
|--------------------|----------|---------------|
| Rendement annuel   | +65 %    | +59 %         |
| Pire chute         | **-42 %**| -84 %         |
| Sharpe             | 1,40     | 1,03          |
| 2018 (krach)       | -12 %    | -73 %         |
| 2022 (krach)       | 0 %      | -64 %         |

Pour refaire le calcul : `python backtest.py`

**Ce qu'il faut savoir sur ces chiffres :**
- **2017 domine le résultat**, et une année pareille ne reviendra peut-être pas. Sans elle, le bot et le BTC font beaucoup moins.
- **Le bot rate une partie des hausses** (par exemple +35 % contre +121 % en 2024). C'est le prix à payer pour éviter les krachs.
- **Une chute de -42 % reste possible.** Il faut être prêt à la vivre sans couper le bot au pire moment.
- **Les performances passées ne garantissent rien.** Le marché crypto de 2026 n'est plus celui de 2017.

## Est-ce que c'est rentable ? Les tests de solidité

Un bon backtest peut venir de la chance. `python robustesse.py` vérifie
que le résultat tient quand on change les conditions :

| Test | Résultat |
|---|---|
| Sans l'année 2017 (2018 à 2026) | Bot **+35 %/an** (pire chute -42 %) contre BTC +22 %/an (pire chute -81 %) |
| Départ un mois au hasard, bilan après 1 an | Bot gagnant dans **75 %** des cas (pire cas -32 %) |
| Bilan après 2 ans | Bot gagnant dans **95 %** des cas (pire cas -23 %) |
| Bilan après 3 ans | Bot gagnant dans **100 %** des cas (pire cas +87 %) |
| 81 réglages différents (2018 à 2026) | **Tous rentables**, de +30 % à +52 %/an |
| 7 cryptos jamais utilisées pour le concevoir | Le bot est positif sur 6 sur 7, et sa pire chute est toujours bien plus faible |
| Frais doublés | Encore +29 %/an sans 2017 |

**La limite :** tous ces tests portent sur l'histoire de la crypto, qui a
beaucoup monté entre 2016 et 2026. Si le marché crypto stagne pendant des
années, le bot gagnera peu, mais il devrait limiter les pertes.

## Mise en route

### Étape 1 : tester en simulation (aucun compte nécessaire)

```bash
pip install -r requirements.txt
python backtest.py      # résultats sur l'historique
python bot.py           # une journée de trading avec 1 000 € fictifs
```

L'état du portefeuille fictif est enregistré dans `paper_state.json` et chaque
ordre est noté dans `journal.csv`.

Le bot doit se lancer **chaque jour vers 00 h 05 UTC**, juste après la clôture
de la bougie journalière. Sur Mac ou Linux, ouvre la liste des tâches avec
`crontab -e` et ajoute la ligne suivante :

```
5 0 * * * cd /chemin/vers/trading-bot && python3 bot.py >> bot.log 2>&1
```

Sur Windows, utilise le Planificateur de tâches. Si ton ordinateur n'est pas
toujours allumé, un petit serveur VPS à environ 5 €/mois fait l'affaire.

👉 **Laisse tourner la simulation au moins 1 à 3 mois** avant de passer au réel.

### Étape 2 : ouvrir un compte Kraken

1. Crée un compte sur **kraken.com**.
2. Vérifie ton identité (carte d'identité + justificatif de domicile, niveau « Intermediate »).
3. Active la **double authentification (2FA)** avec une application comme Google Authenticator ou Authy.
4. Dépose des euros par **virement SEPA**. Le virement est gratuit ou presque, contrairement à la carte bancaire.
5. Crée une **clé API** dans *Paramètres → API*. Coche **uniquement** :
   - ✅ *Query Funds* (consulter le solde)
   - ✅ *Create & Modify Orders* (passer des ordres)
   - ❌ **jamais** *Withdraw Funds* (retirer des fonds) : si la clé est volée, personne ne pourra vider ton compte.

### Étape 3 : passer au réel, avec une petite somme

```bash
export KRAKEN_API_KEY="ta_clé"
export KRAKEN_API_SECRET="ton_secret"
export MAX_CAPITAL_EUR=200         # le bot ne gère jamais plus que cette somme
python bot.py --live --dry-run     # montre les ordres SANS les exécuter
python bot.py --live               # trade pour de vrai
```

Ne mets jamais tes clés dans un fichier envoyé sur GitHub.

## Impôts (France)

- Les plus-values sont imposées au moment où tu **revends des cryptos contre des euros**, avec la flat tax de 30 %. Les échanges entre cryptos ne sont pas imposés.
- Un compte sur une plateforme étrangère comme Kraken doit être **déclaré** chaque année avec le formulaire **3916-bis**. L'amende en cas d'oubli est de 750 € par compte.
- Garde `journal.csv` : il liste toutes les opérations.

## Les fichiers

| Fichier | Rôle |
|---|---|
| `strategy.py` | La stratégie (les 4 règles) |
| `backtest.py` | Le test sur l'historique depuis 2016 |
| `bot.py` | Le bot à lancer chaque jour |
| `data.py` | Le téléchargement des cours (API publiques Coinbase et Kraken) |
| `kraken.py` | La connexion au compte Kraken (solde et ordres) |

⚠️ Ce bot est un outil, pas une promesse de gains. N'investis que ce que tu peux perdre.
