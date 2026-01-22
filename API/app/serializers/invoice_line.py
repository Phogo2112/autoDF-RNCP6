from rest_framework import serializers
from app.models import InvoiceLine  

class InvoiceLineSerializer(serializers.ModelSerializer):
    vat_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        source='calculate_vat'
    )
    
    class Meta:
        model = InvoiceLine
        fields = [
            'id',
            'invoice',
            'description',
            'line_type',
            'quantity',
            'price_unit',
            'taux_vat', 
            'amount_et',
            'vat_amount',
            'note'
        ]
        read_only_fields = ['id', 'amount_et', 'vat_amount']
    
    def validate(self, data):
        if self.instance and not self.instance.invoice.is_editable():
            raise serializers.ValidationError(
                f"Cette facture ne peut plus être modifiée (statut: {self.instance.invoice.get_status_display()})"
            )
        return data