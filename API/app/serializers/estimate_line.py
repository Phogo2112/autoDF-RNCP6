from rest_framework import serializers
from app.models import EstimateLine

class EstimateLineSerializer(serializers.ModelSerializer):
    vat_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        source='calculate_vat'
    )
    
    class Meta:
        model = EstimateLine
        fields = [
            'id',
            'estimate',
            'description',
            'line_type',
            'quantity',
            'price_unit',
            'rate_vat',
            'amount_et',
            'vat_amount',
            'note'
        ]
        read_only_fields = ['id', 'amount_et', 'vat_amount']
    
    def validate(self, data):
        """Empêche la modification si le devis n'est plus en brouillon"""
        if self.instance and not self.instance.estimate.is_editable():
            raise serializers.ValidationError(
                f"Ce devis ne peut plus être modifié (statut: {self.instance.estimate.get_status_display()})"
            )
        return data