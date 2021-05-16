from rest_framework import serializers

from core.models import Aplicacao, Ativo


class AplicacaoSerializer(serializers.ModelSerializer):
    """Serializer for aplicação objects"""
    ativos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ativo.objects.all()
    )

    class Meta:
        model = Aplicacao
        fields = ('id', 'date_solicitation', 'quantity', 'value', 'ativos')
        read_only_fields = ('id', )
