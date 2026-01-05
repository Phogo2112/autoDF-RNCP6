from rest_framework import viewsets
from app.models import Estimate
from app.serializers import EstimateSerializer

class EstimateViewSet(viewsets.ModelViewSet):
  queryset = Estimate.objects.all()
  serializer_class = EstimateSerializer