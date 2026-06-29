"""
Conversion des dates stockées en UTC vers l'heure de Paris pour l'affichage.

Toutes les dates en base (kickoff_at) restent en UTC — c'est la bonne pratique
pour stocker des dates (pas d'ambiguïté, pas de souci si on ajoute un jour des
joueurs dans d'autres fuseaux horaires). La conversion vers l'heure locale se
fait uniquement à l'affichage, via le filtre Jinja `paris_time` défini ici.

On utilise zoneinfo (bibliothèque standard depuis Python 3.9, pas de
dépendance supplémentaire à installer) plutôt qu'un simple décalage fixe
"+2h", parce que Paris bascule entre UTC+1 (heure d'hiver, CET) et UTC+2
(heure d'été, CEST) selon la période de l'année — zoneinfo gère ce
basculement automatiquement, un décalage fixe serait faux la moitié de l'année.
"""
from datetime import timezone
from zoneinfo import ZoneInfo

PARIS_TZ = ZoneInfo("Europe/Paris")


def to_paris_time(dt):
    """
    Convertit un datetime (supposé en UTC, naïf ou avec tzinfo) vers l'heure
    de Paris. Utilisé comme filtre Jinja : {{ match.kickoff_at | paris_time }}

    Si dt est naïf (sans tzinfo, cas des dates lues depuis certaines bases),
    on suppose qu'il est en UTC avant de convertir — cohérent avec le
    commentaire déjà présent sur Match.kickoff_at ("toujours en UTC").
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(PARIS_TZ)


def format_paris_time(dt, fmt="%d/%m %H:%M"):
    """
    Filtre Jinja tout-en-un : convertit en heure de Paris ET formate en une
    seule étape, pour remplacer directement les usages existants de
    `match.kickoff_at.strftime(...)` dans les templates par
    `match.kickoff_at | paris_datetime` sans avoir à chaîner deux filtres.
    """
    converted = to_paris_time(dt)
    if converted is None:
        return ""
    return converted.strftime(fmt)
