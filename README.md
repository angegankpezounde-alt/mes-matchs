# Mes Matchs — Calendrier multi-compétitions (test rapide)

Page statique unique, sans compte, sans base de données : affiche tous les
matchs des compétitions suivies (Coupe du Monde pour l'instant), en heure de
Paris, sur les 10 prochains jours.

## Tester en local

```bash
pip install requests --break-system-packages
export FOOTBALL_DATA_API_KEY=ta_cle_ici
python generate.py
```

Ça génère un fichier `index.html` — ouvre-le simplement dans ton navigateur
pour voir le résultat.

## Ajouter une compétition

Édite la liste `COMPETITIONS` au début de `generate.py` :

```python
COMPETITIONS = [
    {"code": "WC", "name": "Coupe du Monde 2026", "icon": "🌍"},
    {"code": "FL1", "name": "Ligue 1", "icon": "🇫🇷"},  # à ajouter dès la reprise
]
```

## Déployer gratuitement avec GitHub Pages + mise à jour automatique

1. Crée un repo GitHub **public** (Pages gratuit nécessite un repo public)
2. Pousse tous ces fichiers, y compris le dossier `.github/workflows/`
3. Configure ta clé API comme secret du repo :
   - Settings → Secrets and variables → Actions → New repository secret
   - Nom : `FOOTBALL_DATA_API_KEY`
   - Valeur : ta clé football-data.org
4. Active GitHub Pages :
   - Settings → Pages → Source : "Deploy from a branch" → branche `main`, dossier `/ (root)`
5. Le fichier `index.html` sera régénéré automatiquement toutes les heures par
   la GitHub Action (`.github/workflows/update.yml`) — tu peux aussi la
   déclencher manuellement depuis l'onglet "Actions" du repo en attendant la
   prochaine heure pile.
6. Ton site est en ligne à `https://ton-pseudo.github.io/nom-du-repo/`

## Limitations volontaires de ce test (à ne PAS corriger tout de suite)

- Pas de personnalisation (équipes favorites) — on regarde si même une
  version générique attire du monde
- Mise à jour manuelle (relancer le script) — l'automatisation via GitHub
  Actions est prévue seulement si ce test montre un signal positif
- Une seule compétition pour l'instant (Coupe du Monde)

## Critère de succès (à évaluer après 1 semaine)

- Toi-même : tu reviens dessus naturellement plutôt que sur tes anciennes
  habitudes
- ~50 visiteurs uniques sur la semaine (hors toi-même)
- 2-3 retours qualitatifs positifs sur le post Reddit de lancement
