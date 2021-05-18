from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from aplication.serializers import AplicacaoSerializer
from core.models import Aplicacao


class CreateAplicationView(generics.ListCreateAPIView):
    """Create a new aplicação in the system"""
    serializer_class = AplicacaoSerializer
    queryset = Aplicacao.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the aplicação for the authenticated user"""
        ativos = self.request.query_params.get('ativos')
        queryset = self.queryset
        if ativos:
            ativo_ids = self._params_to_ints(ativos)
            queryset = queryset.filter(ativos__id__in=ativo_ids)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new aplicação"""
        serializer.save(user=self.request.user)
