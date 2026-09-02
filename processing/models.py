from django.conf import settings
from django.db import models
from images_app.models import Image


class AIProcess(models.Model):
    """Un traitement IA appliqué à une image (cf. S21 + S15 Historique)."""

    class TypeTraitement(models.TextChoices):
        SUPPRESSION_FOND = 'suppression_fond', "Suppression d'arrière-plan"
        EFFACEMENT_OBJET = 'effacement_objet', 'Effacement d’objet'
        AMELIORATION = 'amelioration', 'Amélioration de la qualité'
        UPSCALING = 'upscaling', 'Agrandissement'
        RESTAURATION = 'restauration', 'Restauration de photo'
        GENERATION = 'generation', "Génération d'image"
        TRANSFORMATION = 'transformation', 'Transformation artistique'

    class Statut(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'En attente'
        EN_COURS = 'en_cours', 'En cours'
        TERMINE = 'termine', 'Disponible'
        ECHEC = 'echec', 'Échec'

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='traitements')
    type_traitement = models.CharField(max_length=30, choices=TypeTraitement.choices)
    statut = models.CharField(max_length=15, choices=Statut.choices, default=Statut.EN_ATTENTE)
    message_erreur = models.CharField(max_length=255, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.type_traitement} — {self.statut} — {self.utilisateur.email}"
