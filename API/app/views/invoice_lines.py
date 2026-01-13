from rest_framework import viewsets
from app.models import InvoiceLines
from app.serializers import InvoiceLinesSerializer

class InvoiceLinesViewSet(viewsets.ModelViewSet):
    queryset = InvoiceLines.objects.all()
    serializer_class = InvoiceLinesSerializer