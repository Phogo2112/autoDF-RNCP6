from rest_framework import serializers
from app.models import *


#  hashage de mdp sur le user en bdd et possibilité de modifier le mdp sous demande.


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



class EstimateInvoiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = invoice_estimate
    fields = ['id', 'price_ht', 'price_tva', 'price_ttc', 'created_at', 'users_id', 'clients_id', 'name_estimate_invoice']
    read_only_fields = ['id', 'created_at', 'users_id', 'clients_id']


class StatisticsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Statistics
    fields = ['id', 'price_ht', 'price_tva', 'price_ttc']
    read_only_fields = ['id']