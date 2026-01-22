from rest_framework import viewsets
from app.models import Client
from app.serializers.client import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer