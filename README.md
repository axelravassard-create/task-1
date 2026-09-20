# IELTS Writing Task 1 — jeu de révision

Page HTML **autonome** (`index.html`) : aucune dépendance, aucune bibliothèque externe,
fonctionne hors connexion une fois chargée, sur mobile comme sur ordinateur.
Il suffit d'ouvrir `index.html` dans un navigateur.

## Modes de jeu

| Mode | Contenu |
|---|---|
| 🎴 **Flashcards** | 43 entrées de vocabulaire (anglais ↔ français, sens choisissable ou aléatoire) + 45 fiches de méthodologie. Carte à retourner, boutons « Je sais » / « À revoir », filtrage par catégorie ou par thème. |
| ❓ **Quiz** | QCM généré à la volée sur le **vocabulaire** (distracteurs pris dans la même catégorie pour forcer la précision) **et** sur la **méthodologie** (structure, minutage, type de graphique, sélection des données, grammaire, exemple annoté). |
| 🗂️ **Classement rapide** | Ranger chaque expression dans sa catégorie (hausse, baisse, stabilité, degré, comparaison, approximation, temps, process, maps, introduction, overview, nom de tendance), avec chrono de 10 s et bonus de rapidité (mode sans chrono disponible). |
| 📘 **Mémo** | La fiche complète : structure et minutage, méthodologie par type de graphique, règle des 4 à 6 éléments, grammaire spécifique, exemple annoté bon vs mauvais overview, et tout le vocabulaire en tableaux. |
| 📈 **Progrès** | Score, série, précision, meilleure série, maîtrise globale, barre de maîtrise par catégorie et liste « à revoir en priorité ». |

## Répétition espacée

Chaque notion porte un poids. Une erreur multiplie ce poids par ~2,6 (la notion revient
beaucoup plus vite), une bonne réponse le divise par ~1,8. Une notion est *maîtrisée*
après 3 bonnes réponses d'affilée et n'apparaît alors plus que rarement.
Le tirage des questions est pondéré par ces poids, avec une garde contre les répétitions
immédiates.

Score, poids et progression sont sauvegardés dans le `localStorage` du navigateur
(bouton de réinitialisation dans l'onglet Progrès). Thème clair / sombre inclus.
