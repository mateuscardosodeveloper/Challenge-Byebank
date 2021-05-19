from rest_framework import serializers

from core.models import Resgate, Ativo


class ResgateSerializer(serializers.ModelSerializer):
    """Serializers for resgate objects"""
    ativos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ativo.objects.all()
    )

    class Meta:
        model = Resgate
        fields = ('date_solicitation', 'quantity', 'value', 'ativos')
        read_only_fields = ('quantity', )
