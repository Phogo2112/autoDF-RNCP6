from rest_framework import viewsets
from app.models import Home
from app.serializers import HomeSerializer

class HomeViewSet(viewsets.ModelViewSet):
  queryset = Home.objects.all()
  serializer_class = HomeSerializer