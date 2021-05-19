from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from redeem.serializers import ResgateSerializer
from core.models import Resgate


class CreateResgateView(generics.ListCreateAPIView):
    """Viewer resgate in the system"""
    serializer_class = ResgateSerializer
    queryset = Resgate.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new aplicação"""
        serializer.save(user=self.request.user)
