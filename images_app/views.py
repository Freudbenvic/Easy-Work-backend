from rest_framework import viewsets, permissions
from .models import Image
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/images/          — galerie "Mes images" (S14)
    GET /api/images/{id}/
    DELETE /api/images/{id}/  — suppression d'une image (S14 + MVP S32)
    """

    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'delete', 'head', 'options']

    def get_queryset(self):
        return Image.objects.filter(utilisateur=self.request.user)

    def destroy(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework import status
        instance = self.get_object()
        instance.fichier_original.delete(save=False)
        if instance.fichier_resultat:
            instance.fichier_resultat.delete(save=False)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
