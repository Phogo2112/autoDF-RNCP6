from rest_framework import serializers
from app.models import Users, Clients, Estimates, EstimateLines, Invoices, InvoiceLines


#  hashage de mdp sur le user en bdd et possibilité de modifier le mdp sous demande.


class UsersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ['id','firstname','lastname','email','number_phone','name_business']
    write_only_fields = ['password']
    read_only_fields = ['id','created_at','updated_at','last_login','users_id','modified_at']
    
  def create(self, validated_data):
    password = validated_data.pop("password")
    user = Users(**validated_data)
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
class ClientsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Clients
    fields = ['id','client_type','name','first_name','last_name','address','postal_code','email','mobile','users_id']
    read_only_fields = ['id','created_at','updated_at','last_login','users_id','created_by','modified_at']


class EstimatesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Estimates
    fields = ['id','client','price_et','price_vat','price_ati','sent','sent_date','users_id','modified_at']
    read_only_fields = ['id','created_at','updated_at','last_login','users_id','created_by','sent','sent_date','modified_at']

class EstimateLinesSerializer(serializers.ModelSerializer):
  class Meta:
    model = EstimateLines
    fields = ['id','client','estimate','product','quantity','price_unit','price_total','users_id','sent','sent_date','modified_at']
    read_only_fields = ['id','created_at','updated_at','last_login','users_id','created_by','modified_at']


class InvoiceLinesSerializer(serializers.ModelSerializer):
  class Meta:
    model = InvoiceLines
    fields = ['id','invoice','product','quantity','price_unit','price_total','users_id','sent','sent_date','modified_at']
    read_only_fields = ['id','created_at','updated_at','last_login','users_id','created_by','modified_at']

class InvoicesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Invoices
    fields = ['id','invoice','product','quantity','price_unit','price_total','users_id','sent','sent_date','modified_at']
    read_only_fields = ['id','created_at','updated_at','last_login','users_id','created_by','modified_at']
