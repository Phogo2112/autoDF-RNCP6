from rest_framework import viewsets
from app.models import EstimateLine
from app.serializers import EstimateLineSerializer

class EstimateLineViewSet(viewsets.ModelViewSet):
  queryset = EstimateLine.objects.all()
  serializer_class = EstimateLineSerializer