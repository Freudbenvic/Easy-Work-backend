from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Credit


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_credit_for_new_user(sender, instance, created, **kwargs):
    if created:
        Credit.objects.create(utilisateur=instance, solde=10)
