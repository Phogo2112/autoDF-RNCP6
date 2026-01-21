from rest_framework import viewsets
from app.models import Invoices
from app.serializers import InvoicesSerializer

class InvoicesViewSet(viewsets.ModelViewSet):
    queryset = Invoices.objects.all()
    serializer_class = InvoicesSerializer