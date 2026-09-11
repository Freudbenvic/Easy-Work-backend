from django.conf import settings
from django.db import models
from images_app.models import Image


class Favorite(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['utilisateur', 'image']
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.utilisateur.email} - image #{self.image_id}"
