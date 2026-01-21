from rest_framework import viewsets
from app.models import Estimates
from app.serializers import EstimatesSerializer

class EstimatesViewSet(viewsets.ModelViewSet):
    queryset = Estimates.objects.all()
    serializer_class = EstimatesSerializer