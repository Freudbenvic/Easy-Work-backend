from django.conf import settings
from django.db import models


class Image(models.Model):
    """Une image importée par un utilisateur, avec son résultat éventuel (cf. S21)."""

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images'
    )
    fichier_original = models.ImageField(upload_to='originals/%Y/%m/')
    fichier_resultat = models.ImageField(upload_to='results/%Y/%m/', null=True, blank=True)
    outil = models.CharField(max_length=50, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"Image #{self.pk} — {self.utilisateur.email}"
