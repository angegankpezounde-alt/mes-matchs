"""
Générateur de page statique : calendrier de matchs multi-compétitions.

Pas de Flask, pas de base de données, pas de compte utilisateur — ce script
appelle football-data.org, génère un fichier index.html unique et statique,
et c'est tout. On le relance manuellement (ou via une tâche planifiée gratuite
type GitHub Actions) pour rafraîchir les données.

Objectif explicite : tester en quelques heures si "voir tous mes matchs/
compétitions favoris en une seule vue épurée, en heure de Paris" attire du
monde — avant d'investir plus de temps dans une vraie app avec compte,
personnalisation, etc.

Usage :
    FOOTBALL_DATA_API_KEY=ta_cle python generate.py
"""
import os
import sys
from datetime import datetime, timedelta, timezone

from football_api import FootballDataClient
from flags import get_flag_url
from timezones import format_paris_time

# Compétitions suivies pour ce test — codes football-data.org.
# WC = Coupe du Monde. On pourra ajouter FL1 (Ligue 1), CL (Champions League)
# dès leur reprise, simplement en complétant cette liste.
COMPETITIONS = [
    {"code": "WC", "name": "Coupe du Monde 2026", "icon": "🌍"},
]

WINDOW_DAYS_PAST = 1   # matchs très récents (hier) encore montrés un peu
WINDOW_DAYS_FUTURE = 10  # matchs à venir affichés jusqu'à 10 jours


def fetch_all_matches(api_key):
    """Récupère les matchs de toutes les compétitions suivies, fusionnés."""
    client = FootballDataClient(api_key)
    all_matches = []
    for comp in COMPETITIONS:
        try:
            raw_matches = client.get_matches(competition_code=comp["code"])
        except Exception as e:
            print(f"Erreur sur {comp['name']} : {e}", file=sys.stderr)
            continue
        for m in raw_matches:
            all_matches.append({
                "competition_name": comp["name"],
                "competition_icon": comp["icon"],
                "home_team": m.get("homeTeam", {}).get("name") or "?",
                "away_team": m.get("awayTeam", {}).get("name") or "?",
                "stage": m.get("stage", ""),
                "utc_date": m["utcDate"],
                "status": m.get("status", ""),
                "home_score": m.get("score", {}).get("fullTime", {}).get("home"),
                "away_score": m.get("score", {}).get("fullTime", {}).get("away"),
            })
    return all_matches


def filter_to_window(matches):
    """Garde seulement les matchs dans la fenêtre [hier, +10 jours]."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=WINDOW_DAYS_PAST)
    end = now + timedelta(days=WINDOW_DAYS_FUTURE)

    kept = []
    for m in matches:
        kickoff = datetime.fromisoformat(m["utc_date"].replace("Z", "+00:00"))
        if start <= kickoff <= end:
            m["_kickoff_dt"] = kickoff
            kept.append(m)
    kept.sort(key=lambda m: m["_kickoff_dt"])
    return kept


def render_match_card(m):
    flag_home = get_flag_url(m["home_team"]) or ""
    flag_away = get_flag_url(m["away_team"]) or ""
    paris_time = format_paris_time(m["_kickoff_dt"])

    is_live = m["status"] in ("IN_PLAY", "PAUSED")
    is_finished = m["status"] == "FINISHED"

    if is_finished and m["home_score"] is not None:
        score_html = f'<span class="score">{m["home_score"]} - {m["away_score"]}</span>'
        status_badge = '<span class="badge badge-finished">Terminé</span>'
    elif is_live:
        score_html = '<span class="score score-live">— vs —</span>'
        status_badge = '<span class="badge badge-live">🔴 En direct</span>'
    else:
        score_html = '<span class="score score-pending">vs</span>'
        status_badge = ""

    home_flag_html = f'<img src="{flag_home}" class="flag" alt="">' if flag_home else ""
    away_flag_html = f'<img src="{flag_away}" class="flag" alt="">' if flag_away else ""

    return f"""
    <div class="match-card">
        <div class="match-meta">
            <span class="comp-badge">{m['competition_icon']} {m['competition_name']}</span>
            <span class="stage">{m['stage']}</span>
            {status_badge}
        </div>
        <div class="match-row">
            <div class="team">{home_flag_html}<span>{m['home_team']}</span></div>
            {score_html}
            <div class="team">{away_flag_html}<span>{m['away_team']}</span></div>
        </div>
        <div class="match-time">{paris_time} (heure de Paris)</div>
    </div>
    """


def render_page(matches):
    cards_html = "\n".join(render_match_card(m) for m in matches)
    if not matches:
        cards_html = '<p class="empty">Aucun match dans les prochains jours.</p>'

    generated_at = datetime.now(timezone.utc).strftime("%d/%m/%Y à %H:%M UTC")

    with open("style.css", encoding="utf-8") as f:
        css = f.read()

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mes Matchs — Calendrier multi-compétitions</title>
    <meta name="description" content="Tous tes matchs de foot favoris, toutes compétitions confondues, en un coup d'œil et en heure de Paris.">
    <style>{css}</style>
</head>
<body>
    <header>
        <h1>⚽ Mes Matchs</h1>
        <p class="subtitle">Toutes tes compétitions, une seule vue, heure de Paris.</p>
    </header>
    <main>
        {cards_html}
    </main>
    <footer>
        <p>Dernière mise à jour : {generated_at}</p>
    </footer>
</body>
</html>"""


def main():
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY", "")
    if not api_key:
        print("ERREUR : variable FOOTBALL_DATA_API_KEY manquante.", file=sys.stderr)
        sys.exit(1)

    print("Récupération des matchs...")
    matches = fetch_all_matches(api_key)
    print(f"{len(matches)} matchs récupérés au total (toutes compétitions).")

    matches = filter_to_window(matches)
    print(f"{len(matches)} matchs dans la fenêtre d'affichage (-1j / +10j).")

    html = render_page(matches)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Fichier index.html généré avec succès.")


if __name__ == "__main__":
    main()
