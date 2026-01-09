from rest_framework import serializers
from app.models import *


#  hashage de mdp sur le user en bdd et possibilité de modifier le mdp sous demande.

# serializer Clients and Users

class ClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Client
    fields = ['id','firstname','lastname','email','number_phone']
    read_only_fields = ['id','firstname','lastname','email','number_phone']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id','firstname','lastname','email','number_phone']
    read_only_fields = ['firstname','lastname','email', 'password','number_phone','id']
    
  def create(self, validated_data):
    password = validated_data.pop("password")
    user = User(**validated_data)
    user.set_password(password)
    user.save()
    return user
    
  def update(self, instance, validated_data):
    password = validated_data.pop('password', None)
    for k, v in validated_data.items():
      setattr(instance, k, v)
    if password:
      instance.set_password(password)
    instance.save()
    return instance 

# serializer invoice

class InvoiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Invoice
    fields = ['id', 'price_et', 'price_vat', 'price_ati','created_at','user_id','client_id','modified_at','sent','sent_date']
    read_only_fields = ['id','created_at','user_id','client_id','modified_at','sent','sent_date']

class InvoiceLineSerializer(serializers.ModelSerializer):
  class Meta:
    model = InvoiceLine
    fields = ['id', 'price_et', 'price_vat', 'price_ati','created_at','user_id','client_id','modified_at','sent','sent_date']
    read_only_fields = ['id','created_at','user_id','client_id','modified_at','sent','sent_date']
  
# serializer estimate

class EstimateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Estimate
    fields = ['id', 'price_et', 'price_vat', 'price_ati','created_at','user_id','client_id','modified_at','sent','sent_date']
    read_only_fields = ['id','created_at','user_id','client_id','modified_at','sent','sent_date']



class EstimateLineSerializer(serializers.ModelSerializer):
  class Meta:
    model = EstimateLine
    fields = ['id', 'price_et', 'price_vat', 'price_ati','created_at','user_id','client_id','modified_at','sent','sent_date']
    read_only_fields = ['id','created_at','user_id','client_id','modified_at','sent','sent_date']