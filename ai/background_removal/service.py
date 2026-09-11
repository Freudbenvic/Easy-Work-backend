"""
Service de suppression d'arrière-plan (cf. cahier des charges S6).

Utilise rembg avec le modèle "isnet-general-use" (~176 Mo, réseau ISNet)
plutôt que RMBG ou MODNet, pour rester 100% open source et fonctionner
sans GPU ni clé d'API. Ce modèle donne des contours nettement plus
propres que le petit "u2netp" utilisé au tout début (mais le premier
appel est un peu plus long : téléchargement unique du modèle).

Le reste du backend (processing/views.py) ne connaît que la fonction
remove_background() ci-dessous : le modèle pourra être changé plus tard
(RMBG-2.0, MODNet...) sans toucher au reste de l'application.
"""

from django.core.files.base import ContentFile

_session = None


def _get_session():
    global _session
    if _session is None:
        from rembg import new_session

        _session = new_session('isnet-general-use')
    return _session


def remove_background(uploaded_file) -> ContentFile:
    from rembg import remove

    uploaded_file.seek(0)
    input_bytes = uploaded_file.read()

    output_bytes = remove(input_bytes, session=_get_session())

    return ContentFile(output_bytes, name='resultat.png')
