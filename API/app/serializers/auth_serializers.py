from rest_framework import serializers
from app.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'password_confirm',
            'name_business',
            'siret',
            'first_name',
            'last_name',
            'address',
            'city',
            'postal_code',
            'mobile'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'name_business': {'required': True},
            'username': {'required': True},
            'siret': {
                'required': True,
                'min_length': 14,
                'max_length': 14,
                'error_messages': {
                    'min_length': 'Le SIRET doit contenir exactement 14 chiffres',
                    'max_length': 'Le SIRET doit contenir exactement 14 chiffres',
                }
            },
        }
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Les mots de passe ne correspondent pas'
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': 'Email ou mot de passe incorrect'
            })
        
        if not user.check_password(password):
            raise serializers.ValidationError({
                'password': 'Email ou mot de passe incorrect'
            })
        
        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
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
        read_only_fields = ['id', 'email', 'created_at', 'updated_at', 'last_login']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'Les nouveaux mots de passe ne correspondent pas'
            })
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Ancien mot de passe incorrect')
        return value
        