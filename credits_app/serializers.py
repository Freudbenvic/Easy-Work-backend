from rest_framework import serializers
from .models import Credit


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ['solde', 'date_mise_a_jour']
