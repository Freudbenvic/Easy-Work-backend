from rest_framework import serializers
from .models import Credit


class CreditSerializer(serializers.ModelSerializer):
    illimite = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        fields = ['solde', 'date_mise_a_jour', 'illimite']

    def get_illimite(self, obj):
        return bool(obj.utilisateur.is_staff)
