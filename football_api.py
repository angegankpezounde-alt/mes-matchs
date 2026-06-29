"""
Client pour football-data.org.

Doc API : https://docs.football-data.org/general/v4/competition.html
Code compétition pour la Coupe du Monde : "WC"
Header d'authentification : X-Auth-Token

Limite tier gratuit : 10 appels/minute. Largement suffisant pour notre usage
(quelques dizaines d'appels ponctuels, pas de polling en continu).
"""
import requests

BASE_URL = "https://api.football-data.org/v4"


class FootballDataClient:
    def __init__(self, api_key):
        # .strip() supprime les espaces et retours à la ligne invisibles qui
        # peuvent se glisser dans un fichier .env (espace en fin de ligne,
        # caractère de fin de fichier...) et qui rendraient le token invalide
        # côté API sans que ce soit visible à l'œil dans un éditeur de texte.
        self.api_key = (api_key or "").strip()
        self.headers = {"X-Auth-Token": self.api_key}

    def get_matches(self, competition_code="WC"):
        """
        Récupère tous les matchs d'une compétition (terminés et à venir).
        Retourne la liste brute de l'API (liste de dicts).
        """
        url = f"{BASE_URL}/competitions/{competition_code}/matches"
        response = requests.get(url, headers=self.headers, timeout=15)
        if not response.ok:
            # On affiche le corps de la réponse (souvent un message explicite,
            # ex: "the resource you are looking for does not exist" ou un détail
            # sur un filtre invalide) plutôt que de juste planter sur le code HTTP.
            raise requests.exceptions.HTTPError(
                f"{response.status_code} {response.reason} pour {url} — "
                f"réponse de l'API : {response.text}"
            )
        data = response.json()
        return data.get("matches", [])

    def get_match(self, match_external_id):
        """Récupère un seul match par son ID football-data.org."""
        url = f"{BASE_URL}/matches/{match_external_id}"
        response = requests.get(url, headers=self.headers, timeout=15)
        response.raise_for_status()
        return response.json()


def extract_score(api_match):
    """
    Extrait (home_score, away_score, status) d'un objet match retourné par l'API.
    Retourne (None, None, "scheduled") si le match n'a pas encore de score.

    Note : l'API distingue plusieurs statuts (SCHEDULED, TIMED, IN_PLAY, PAUSED,
    FINISHED, POSTPONED, ...). Pour la v1 on simplifie en ne gérant que
    "FINISHED" -> "finished", tout le reste -> "scheduled". Un match en cours
    (IN_PLAY) sera donc affiché comme "à venir" jusqu'à son terme — acceptable
    pour une synchro manuelle déclenchée après le match.
    """
    status = api_match.get("status", "")
    score = api_match.get("score", {}).get("fullTime", {})
    home_score = score.get("home")
    away_score = score.get("away")

    if status == "FINISHED" and home_score is not None and away_score is not None:
        return home_score, away_score, "finished"
    return None, None, "scheduled"
