from django.conf import settings
from django.db import models


class Credit(models.Model):
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit'
    )
    solde = models.PositiveIntegerField(default=10)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.utilisateur.email} - {self.solde} crédits"
