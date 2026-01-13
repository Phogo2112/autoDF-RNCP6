from rest_framework import viewsets
from app.models import EstimateLines
from app.serializers import EstimateLinesSerializer

class EstimateLinesViewSet(viewsets.ModelViewSet):
    queryset = EstimateLines.objects.all()
    serializer_class = EstimateLinesSerializer