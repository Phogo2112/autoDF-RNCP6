from rest_framework import viewsets
from app.models import Statistics
from app.serializers import StatisticsSerializer

class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
