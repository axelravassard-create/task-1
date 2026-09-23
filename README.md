# IELTS Writing — jeux de révision (Task 1 &amp; Task 2)

## Le fichier à ouvrir : `ielts.html`

**`ielts.html` contient tout** — les deux jeux de révision, les exercices corrigés et les examens
blancs — dans un **seul fichier**, avec un sélecteur Task 1 / Task 2 / Corrigés / Examens en bas
d'écran. C'est le fichier
à télécharger : aucun autre n'est nécessaire, rien à installer, tout fonctionne hors connexion.

Il est assemblé par `build.py` à partir des trois pages sources ci-dessous, chacune embarquée
dans une iframe (ce qui évite toute collision entre les trois applications). Après toute
modification d'une source, relancer `python3 build.py`.

## Les trois pages sources

Chacune reste utilisable seule, sans dépendance ni bibliothèque externe, sur mobile comme sur
ordinateur (les liens entre elles ne fonctionnent que si les trois fichiers sont dans le même
dossier — d'où `ielts.html`) :

- **`index.html`** — Writing **Task 1** (graphiques, process, maps)
- **`task2.html`** — Writing **Task 2** (essai argumenté)
- **`exam.html`** — **8 examens blancs** au format officiel, avec chronomètre

Le sélecteur en haut de chaque page permet de passer de l'une à l'autre.

## Task 1 — modes de jeu

| Mode | Contenu |
|---|---|
| 🎴 **Flashcards** | 43 entrées de vocabulaire (anglais ↔ français, sens choisissable ou aléatoire) + 45 fiches de méthodologie. Au verso : la traduction, **une mini-illustration SVG** (courbe qui s'envole, camembert, timeline, process, map avant/après…), une note « quand l'utiliser », **deux exemples de phrases IELTS traduits** et **un contre-exemple « à éviter »** avec la raison de l'erreur. Boutons « Je sais » / « À revoir », filtrage par catégorie ou par thème. |
| ❓ **Quiz** | QCM généré à la volée sur le **vocabulaire** (distracteurs pris dans la même catégorie pour forcer la précision) **et** sur la **méthodologie** (structure, minutage, type de graphique, sélection des données, grammaire, exemple annoté). La correction affiche le schéma, la phrase modèle ✅ et la formulation ❌ à éviter. |
| 🗂️ **Classement rapide** | Ranger chaque expression dans sa catégorie (hausse, baisse, stabilité, degré, comparaison, approximation, temps, process, maps, introduction, overview, nom de tendance), avec chrono de 10 s et bonus de rapidité (mode sans chrono disponible). |
| 🖼️ **Illustrations** | 51 schémas SVG dessinés dans la page (aucune image externe) : ils apparaissent au verso des cartes, dans la correction des quiz, dans celle du classement rapide et dans le mémo. |
| 📘 **Mémo** | La fiche complète : structure et minutage, méthodologie par type de graphique, règle des 4 à 6 éléments, grammaire spécifique, exemple annoté bon vs mauvais overview, et tout le vocabulaire en tableaux — chaque entrée accompagnée de ses exemples ✅ et de son piège ❌. |
| 📈 **Progrès** | Score, série, précision, meilleure série, maîtrise globale, barre de maîtrise par catégorie et liste « à revoir en priorité ». |

## Exemples

Près de 200 phrases modèles : 2 exemples traduits par entrée de vocabulaire, un contre-exemple
commenté pour 39 des 43 entrées (`rose BY 12%` vs `rose of 12%`, `level off` vs `remain stable`,
`converted into` vs `replaced by`, `percentage points` vs `percent`, `twice as high as` vs
`two times higher as`…), et une paire ✅ / ❌ pour 37 des 45 questions de méthodologie.

## Répétition espacée

Chaque notion porte un poids. Une erreur multiplie ce poids par ~2,6 (la notion revient
beaucoup plus vite), une bonne réponse le divise par ~1,8. Une notion est *maîtrisée*
après 3 bonnes réponses d'affilée et n'apparaît alors plus que rarement.
Le tirage des questions est pondéré par ces poids, avec une garde contre les répétitions
immédiates.

Score, poids et progression sont sauvegardés dans le `localStorage` du navigateur
(bouton de réinitialisation dans l'onglet Progrès). Thème clair / sombre inclus.

## Task 2 — `task2.html`

La Task 2 pèse **deux tiers** de la note de Writing : la page couvre donc aussi bien la
méthode que la langue.

| Mode | Contenu |
|---|---|
| 🎴 **Flashcards** | 73 entrées de vocabulaire argumentatif (13 fonctions : paraphrase, thèse, opinion, nuance, argument, cause, exemple, concession, ajout, problème, solution, conclusion, collocations thématiques), 62 fiches de méthodologie et les 18 consignes. Verso : illustration, note d'usage, 2 exemples traduits et le contre-exemple commenté. |
| ❓ **Quiz** | QCM sur le vocabulaire et sur la méthodologie : structure, minutage, types de consignes, les 4 critères de notation, erreurs qui plafonnent la note, production d'idées, grammaire de haut niveau, essai modèle. |
| 🎯 **Type de consigne** | 18 consignes réelles à classer parmi les 5 types (opinion, discussion, avantages/inconvénients, problème-solution, two-part). La correction donne le **plan attendu** et le **piège** propre à chaque sujet — c'est le levier de note n°1. |
| 🗂️ **Classement rapide** | Ranger chaque expression dans sa fonction argumentative, chrono de 10 s. |
| 📘 **Mémo** | Structure et minutage (5/30/5), les 5 types de consignes, les 4 critères expliqués, la méthode PEEL, les erreurs qui plafonnent la note, la grammaire pour viser 8+, un **essai modèle annoté paragraphe par paragraphe** (≈ 280 mots) avec sa version faible, une checklist de relecture, et tout le vocabulaire avec ses exemples. |
| 📈 **Progrès** | Maîtrise par fonction, par thème méthodologique et sur les consignes. |

Même moteur que la Task 1 : répétition espacée, score, séries, thème clair/sombre,
progression sauvegardée séparément dans le `localStorage`.

## Exercices corrigés — onglet « 📗 Corrigés »

Les 12 sujets des examens blancs, **entièrement résolus**, pour comprendre la démarche avant de
s'entraîner seul. Pour chacune des 24 tâches, dans l'ordre où on les ferait le jour de l'épreuve :

1. **Identifier le sujet** — type de graphique ou de consigne, et ce qu'il impose.
2. **Repérer l'essentiel** (Task 1 : les 4 à 6 éléments à retenir, chiffres à l'appui) ou
   **trouver et trier les idées** (Task 2 : idées retenues, idées écartées et pourquoi, position).
3. **Faire le plan** — le contenu de chacun des quatre paragraphes.
4. **Les pièges propres à ce sujet.**
5. **Rédiger** — la copie band 9 commentée paragraphe par paragraphe, avec l'analyse des 4 critères.
6. **La même tâche ratée** — une copie réaliste estimée band 5 à 6, puis chacune de ses erreurs :
   la phrase fautive, le problème, le critère touché (TA/TR, CC, LR, GRA).

Même page que les examens (`exam.html#corriges`), sans chronomètre ni zone de saisie.

## Examens blancs — `exam.html`

12 épreuves complètes **au format officiel** (Task 1 + Task 2, 60 minutes), à corriger en
collant le tout dans une conversation Claude.

| # | Task 1 | Task 2 |
|---|---|---|
| 1 | Line graph — sources d'électricité 2005-2025 | Opinion (agree / disagree) |
| 2 | Bar chart — loisirs par tranche d'âge | Discussion des deux vues |
| 3 | Pie charts — dépenses des ménages 2000 vs 2020 | Avantages / inconvénients (`outweigh`) |
| 4 | Table — population de cinq villes, avec projections | Problème & solution |
| 5 | Process diagram — recyclage du verre | Two-part question |
| 6 | Maps — centre-ville avant / après | Opinion (positive or negative) |
| 7 | Mixed charts — effectifs (barres) + satisfaction (courbe) | Discussion des deux vues |
| 8 | Line graph avec projections en pointillés | Opinion (agree / disagree) |
| 9 | Bar chart — accès à internet, cinq pays, 2005 vs 2020 | Avantages / inconvénients |
| 10 | Line graph — chômage dans trois pays, 2008-2024 | Problème & solution |
| 11 | Process diagram — production du café | Two-part question |
| 12 | Maps — une île avant / après un complexe touristique | Discussion des deux vues |

**Conditions réalistes** : formulations officielles mot pour mot (*Summarise the information by
selecting and reporting the main features…*, *Give reasons for your answer…*), mentions
*You should spend about 20/40 minutes on this task*, vrais graphiques avec axes, unités,
légendes et valeurs, **correcteur orthographique désactivé** comme dans le vrai test,
chronomètre de 60 minutes qui rappelle de passer à la Task 2 à 20:00, compteur de mots
masquable (mode papier).

**Modèle band 9 commenté** — chacune des 24 tâches dispose de sa propre réponse modèle,
repliée par défaut (à n'ouvrir qu'après avoir rédigé). Chacune donne : le texte paragraphe par
paragraphe avec, sous chaque paragraphe, **ce qu'il fait et pourquoi** ; une analyse des
**4 critères officiels** citant le texte (pourquoi ce passage vaut un band 9) ; et 5 à 6
**structures réutilisables** avec des trous à remplir. Les 24 modèles dépassent tous le minimum
de mots (Task 1 : 175-209 mots ; Task 2 : 266-302 mots).

**Correction** : le bouton « Copier pour correction » place dans le presse-papier la consigne
officielle, **les données chiffrées du graphique** (pour que la correction vérifie vos chiffres),
votre réponse avec son nombre de mots et le temps écoulé, ainsi que la grille de correction :
note par critère sur les 4 critères officiels, note globale, erreurs corrigées une par une,
version réécrite band 8+ et 3 actions pour progresser. Les réponses sont sauvegardées dans le
navigateur.
