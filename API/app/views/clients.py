from rest_framework import viewsets
from app.models import Clients
from app.serializers import ClientsSerializer

class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer