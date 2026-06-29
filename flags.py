"""
Correspondance entre les noms d'équipes tels que renvoyés par football-data.org
et leur code pays ISO 3166-1 alpha-2 (en minuscules), utilisé pour construire
les URLs de drapeaux via flagcdn.com (https://flagcdn.com/w80/<code>.png).

Couvre les 48 équipes qualifiées pour la Coupe du Monde 2026. Construit à partir
de la liste officielle des qualifiés (FIFA, Wikipedia) recoupée avec les noms
observés dans les réponses réelles de l'API football-data.org pour ce tournoi.

Note : certains noms d'équipes ont des variantes possibles selon les sources
(ex: "Ivory Coast" vs "Côte d'Ivoire", "South Korea" vs "Korea Republic") — on
mappe toutes les variantes plausibles vers le même code pour être robuste.
"""

TEAM_NAME_TO_COUNTRY_CODE = {
    # Hôtes
    "Canada": "ca",
    "Mexico": "mx",
    "United States": "us",
    "USA": "us",

    # UEFA (Europe)
    "Austria": "at",
    "Belgium": "be",
    "Bosnia and Herzegovina": "ba",
    "Bosnia-Herzegovina": "ba",
    "Croatia": "hr",
    "Czechia": "cz",
    "Czech Republic": "cz",
    "England": "gb-eng",
    "France": "fr",
    "Germany": "de",
    "Netherlands": "nl",
    "Norway": "no",
    "Portugal": "pt",
    "Scotland": "gb-sct",
    "Spain": "es",
    "Sweden": "se",
    "Switzerland": "ch",
    "Turkey": "tr",
    "Türkiye": "tr",

    # CONMEBOL (Amérique du Sud)
    "Argentina": "ar",
    "Brazil": "br",
    "Colombia": "co",
    "Ecuador": "ec",
    "Paraguay": "py",
    "Uruguay": "uy",

    # CONCACAF (hors hôtes)
    "Curaçao": "cw",
    "Curacao": "cw",
    "Haiti": "ht",
    "Panama": "pa",

    # CAF (Afrique)
    "Algeria": "dz",
    "Cape Verde": "cv",
    "Cabo Verde": "cv",
    "Cape Verde Islands": "cv",
    "DR Congo": "cd",
    "Congo DR": "cd",
    "Democratic Republic of Congo": "cd",
    "Ivory Coast": "ci",
    "Côte d'Ivoire": "ci",
    "Cote d'Ivoire": "ci",
    "Egypt": "eg",
    "Ghana": "gh",
    "Morocco": "ma",
    "Senegal": "sn",
    "South Africa": "za",
    "Tunisia": "tn",

    # AFC (Asie)
    "Australia": "au",
    "Iraq": "iq",
    "IR Iran": "ir",
    "Iran": "ir",
    "Japan": "jp",
    "Jordan": "jo",
    "Korea Republic": "kr",
    "South Korea": "kr",
    "Qatar": "qa",
    "Saudi Arabia": "sa",
    "Uzbekistan": "uz",

    # OFC (Océanie)
    "New Zealand": "nz",
}


def get_flag_url(team_name, width="w80"):
    """
    Retourne l'URL flagcdn.com du drapeau pour un nom d'équipe donné, ou None
    si le pays n'est pas dans notre table (cas attendu pour des compétitions
    futures avec d'autres équipes, ou en cas de nom inattendu côté API —
    mieux vaut ne pas afficher de drapeau que d'afficher une image cassée).

    width : taille flagcdn.com, ex. "w40", "w80", "w160". Voir leur doc pour
    les tailles disponibles.
    """
    code = TEAM_NAME_TO_COUNTRY_CODE.get(team_name)
    if code is None:
        return None
    return f"https://flagcdn.com/{width}/{code}.png"
