"""
Service de suppression d'arrière-plan (cf. cahier des charges S6).

Utilise rembg (modèle U^2-Net, variante allégée "u2netp" — quelques Mo,
suffisante pour la V1) plutôt que RMBG ou MODNet, pour rester 100%
open source et fonctionner sans GPU ni clé d'API.

Le reste du backend (processing/views.py) ne connaît que la fonction
`remove_background()` ci-dessous : le modèle pourra être changé plus
tard (RMBG-2.0, MODNet...) sans toucher au reste de l'application.
"""

import io
from django.core.files.base import ContentFile

_session = None


def _get_session():
    """Charge le modèle une seule fois (réutilisé entre les requêtes)."""
    global _session
    if _session is None:
        from rembg import new_session

        _session = new_session('u2netp')
    return _session


def remove_background(uploaded_file) -> ContentFile:
    """
    Prend le fichier image uploadé par l'utilisateur (Django UploadedFile)
    et renvoie un ContentFile PNG avec le fond supprimé (transparence),
    prêt à être assigné à `Image.fichier_resultat`.
    """
    from rembg import remove

    uploaded_file.seek(0)
    input_bytes = uploaded_file.read()

    output_bytes = remove(input_bytes, session=_get_session())

    return ContentFile(output_bytes, name='resultat.png')
