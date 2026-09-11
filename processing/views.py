from django.db.models import F
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from credits_app.models import Credit
from images_app.models import Image
from images_app.serializers import ImageSerializer
from .models import AIProcess
from .serializers import AIProcessSerializer, BackgroundRemovalUploadSerializer

COUT_SUPPRESSION_FOND = 1


class BackgroundRemovalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        upload_serializer = BackgroundRemovalUploadSerializer(data=request.data)
        upload_serializer.is_valid(raise_exception=True)
        fichier = upload_serializer.validated_data['fichier']

        credit, _ = Credit.objects.get_or_create(utilisateur=request.user)
        is_illimite = request.user.is_staff or request.user.is_superuser
        if not is_illimite and credit.solde < COUT_SUPPRESSION_FOND:
            return Response({'detail': 'Crédits insuffisants.'}, status=status.HTTP_402_PAYMENT_REQUIRED)

        image = Image.objects.create(
            utilisateur=request.user,
            fichier_original=fichier,
            outil=AIProcess.TypeTraitement.SUPPRESSION_FOND,
        )
        process = AIProcess.objects.create(
            utilisateur=request.user,
            image=image,
            type_traitement=AIProcess.TypeTraitement.SUPPRESSION_FOND,
            statut=AIProcess.Statut.EN_COURS,
        )

        try:
            from ai.background_removal.service import remove_background

            resultat = remove_background(image.fichier_original)
            image.fichier_resultat.save(resultat.name, resultat, save=True)

            process.statut = AIProcess.Statut.TERMINE
            process.date_fin = timezone.now()
            process.save(update_fields=['statut', 'date_fin'])

            if not is_illimite:
                Credit.objects.filter(pk=credit.pk).update(solde=F('solde') - COUT_SUPPRESSION_FOND)
        except Exception as exc:  # noqa: BLE001
            process.statut = AIProcess.Statut.ECHEC
            process.message_erreur = str(exc)[:255]
            process.date_fin = timezone.now()
            process.save(update_fields=['statut', 'message_erreur', 'date_fin'])
            return Response(
                {'detail': 'Une erreur est survenue pendant le traitement. Veuillez réessayer.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                'image': ImageSerializer(image, context={'request': request}).data,
                'traitement': AIProcessSerializer(process).data,
            },
            status=status.HTTP_201_CREATED,
        )


class HistoriqueView(generics.ListAPIView):
    serializer_class = AIProcessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AIProcess.objects.filter(utilisateur=self.request.user)
