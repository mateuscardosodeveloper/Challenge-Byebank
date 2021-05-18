from rest_framework import serializers

from core.models import Ativo, Modalidade


class ModalidadeSerializer(serializers.ModelSerializer):
    """Serializers for Modalidade objects"""

    class Meta:
        model = Modalidade
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AtivosSerializer(serializers.ModelSerializer):
    """Serializers for Ativos objects"""
    modalidades = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Modalidade.objects.all()
    )

    class Meta:
        model = Ativo
        fields = ('id', 'name', 'modalidades')
        read_only_fields = ('id',)


class AtivosDetailSerializer(AtivosSerializer):
    """Serializer a ativos detail"""
    modalidades = ModalidadeSerializer(many=True, read_only=True)
