from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Modalidade, Ativo


from finance import serializers


class ModalidadeViewSet(viewsets.ModelViewSet):
    """Manage modalidade in the database"""
    queryset = Modalidade.objects.all()
    serializer_class = serializers.ModalidadeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(ativo__isnull=False)

        return queryset.filter().order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class AtivoViewSet(viewsets.ModelViewSet):
    """Manage ativos in the database"""
    serializer_class = serializers.AtivoSerializer
    queryset = Ativo.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the ativos for the authenticated user"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        modalidades = self.request.query_params.get('modalidades')
        queryset = self.queryset
        if modalidades:
            modalidade_ids = self._params_to_ints(modalidades)
            queryset = queryset.filter(modalidades__id__in=modalidade_ids)
        elif assigned_only:
            queryset = queryset.filter(aplicacao__isnull=False)

        return queryset.filter()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.AtivoDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new ativo"""
        serializer.save(user=self.request.user)
