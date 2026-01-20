from rest_framework import viewsets
from app.models import InvoiceLine
from app.serializers.invoice_line import InvoiceLineSerializer

class InvoiceLineViewSet(viewsets.ModelViewSet):
    queryset = InvoiceLine.objects.all()
    serializer_class = InvoiceLineSerializer