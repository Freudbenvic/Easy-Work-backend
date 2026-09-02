from rest_framework import serializers
from images_app.serializers import ImageSerializer
from .models import AIProcess


class AIProcessSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = AIProcess
        fields = [
            'id', 'image', 'type_traitement', 'statut',
            'message_erreur', 'date_creation', 'date_fin',
        ]
        read_only_fields = fields


class BackgroundRemovalUploadSerializer(serializers.Serializer):
    fichier = serializers.ImageField()
