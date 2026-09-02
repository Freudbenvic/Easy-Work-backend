from rest_framework import serializers
from images_app.serializers import ImageSerializer
from images_app.models import Image
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    image_detail = ImageSerializer(source='image', read_only=True)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'image', 'image_detail', 'date_creation']
        read_only_fields = ['id', 'date_creation']

    def validate_image(self, value):
        request = self.context['request']
        if value.utilisateur_id != request.user.id:
            raise serializers.ValidationError("Cette image ne vous appartient pas.")
        return value

    def create(self, validated_data):
        validated_data['utilisateur'] = self.context['request'].user
        return super().create(validated_data)
