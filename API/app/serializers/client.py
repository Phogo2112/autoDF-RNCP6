from rest_framework import serializers
from app.models import Client

class ClientSerializer(serializers.ModelSerializer):
  
    created_by_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Client
        fields = [
            'id',
            'client_type',
            'user',
            'created_by_email',
            'email',
            'mobile',
            'address',
            'city',
            'postal_code',
            'first_name',
            'last_name',
            'name_organisation',
            'siret',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_email']
        extra_kwargs = {
            'email': {'required': True},
            'address': {'required': True},
            'city': {'required': True},
            'postal_code': {'required': True}
        }
    
    def validate(self, data):
        client_type = data.get('client_type')
        
        if client_type == 'individual':
            if not data.get('first_name') or not data.get('last_name'):
                raise serializers.ValidationError({
                    'first_name': 'Le prénom et le nom sont requis pour un particulier',
                    'last_name': 'Le prénom et le nom sont requis pour un particulier'
                })
            if data.get('siret'):
                raise serializers.ValidationError({
                    'siret': 'Un particulier ne peut pas avoir de SIRET'
                })
        
        elif client_type == 'business':
            if not data.get('name_organisation'):
                raise serializers.ValidationError({
                    'name_organisation': "Le nom de l'entreprise est requis"
                })
            if not data.get('siret'):
                raise serializers.ValidationError({
                    'siret': 'Une entreprise doit avoir un numéro SIRET'
                })
        
        return data