from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()


class Command(BaseCommand):
    help = "Promeut un compte existant en administrateur (crédits illimités, accès à /admin/)."

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help="E-mail du compte à promouvoir")

    def handle(self, *args, **options):
        email = options['email']
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise CommandError(f"Aucun utilisateur avec l'e-mail '{email}'.")

        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=['is_staff', 'is_superuser'])

        self.stdout.write(self.style.SUCCESS(f"{email} est maintenant administrateur (crédits illimités)."))
