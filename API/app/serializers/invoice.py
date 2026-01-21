from rest_framework import serializers
from app.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_line = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    created_by_email = serializers.EmailField(source='user.email', read_only=True)
    is_editable = serializers.BooleanField(read_only=True, source='is_editable')
    
    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'client',
            'client_name',
            'user',
            'created_by_email',
            'status',
            'is_editable',
            'price_et',
            'price_vat',
            'price_ati',
            'sent_date',
            'payements_method',
            'payment_date',
            'created_at',
            'modified_at',
            'invoice_line'
        ]
        read_only_fields = [
            'id',
            'price_et',
            'price_vat',
            'price_ati',
            'created_at',
            'modified_at',
            'client_name',
            'created_by_email',
            'is_editable',
            'invoice_line'
        ]
    
    def get_client_name(self, obj):
        if obj.client.client_type == 'individual':
            return f"{obj.client.first_name} {obj.client.last_name}"
        return obj.client.name_organisation
    
    def get_invoice_lines(self, obj):
        from app.serializers.invoice_line import InvoiceLineSerializer
        lines = obj.invoice_line.all()
        return InvoiceLineSerializer(lines, many=True).data
    
    def validate(self, data):
        if self.instance and not self.instance.is_editable():
            allowed_fields = {'status'}
            attempted_changes = set(data.keys()) - allowed_fields
            
            if attempted_changes:
                raise serializers.ValidationError(
                    f"Cette facture ne peut plus être modifiée (statut: {self.instance.get_status_display()}). "
                    f"Seul le statut peut être changé."
                )
        
        return data