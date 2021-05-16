from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from aplication.serializers import AplicacaoSerializer
from core.models import Aplicacao


class CreateAplicationView(generics.CreateAPIView):
    """Create a new aplicação in the system"""
    serializer_class = AplicacaoSerializer
    queryset = Aplicacao.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        """Create a new aplicação"""
        serializer.save(user=self.request.user)
