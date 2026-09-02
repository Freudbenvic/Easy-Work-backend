from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    est_favori = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            'id', 'fichier_original', 'fichier_resultat', 'outil',
            'date_creation', 'est_favori',
        ]
        read_only_fields = fields

    def get_est_favori(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.favorite_set.filter(utilisateur=request.user).exists()
