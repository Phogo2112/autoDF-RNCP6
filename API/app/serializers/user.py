from rest_framework import serializers
from app.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'name_business',
            'siret',
            'first_name',
            'last_name',
            'address',
            'city',
            'postal_code',
            'mobile',
            'created_at',
            'updated_at',
            'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']
        extra_kwargs = {
            'email': {'required': True},
            'name_business': {'required': True},
            'siret': {'required': True}
        }
    
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance