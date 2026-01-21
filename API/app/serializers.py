from rest_framework import serializers
from app.models import Users, Clients, Estimates, EstimateLines, Invoices, InvoiceLines


#  hashage de mdp sur le user en bdd et possibilité de modifier le mdp sous demande.


class UsersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ['id','firstname','lastname','email','number_phone','name_organisation','password','siret',]
    password = serializers.CharField(write_only=True)
    read_only_fields = ['id','created_at','updated_at','last_login','users_id','modified_at',]
    
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
    fields = ['id','client_type','name_organisation','first_name','last_name','address','postal_code','email','mobile','users_id','created_at','updated_at','siret']
    read_only_fields = ['id','created_at','updated_at','users_id','modified_at','created_at','siret','updated_at']


class EstimatesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Estimates
    fields = ['id','clients_id','price_et','price_vat','price_ati','sent','sent_date','users_id','modified_at','created_at']
    read_only_fields = ['id','created_at','users_id','created_by','sent','sent_date','modified_at','total_price','price_vat','price_ati','price_et','clients_id']

class EstimateLinesSerializer(serializers.ModelSerializer):
  class Meta:
    model = EstimateLines
    fields = ['id','client','estimate','product','quantity','price_unit','price_total','users_id','sent','sent_date']
    read_only_fields = ['id','created_at','users_id','created_by','modified_at','sent_date',]


class InvoicesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Invoices
    fields = ['id','invoice','product','quantity','price_unit','price_total','users_id','sent','sent_date','modified_at','payement_methode','payments_date','clients_id','users_id',]
    read_only_fields = ['id','created_at','users_id','created_at','modified_at','clients_id','users_id','sent','sent_date','invoice_number','price_ati','price_vat','price_et',]

class InvoiceLinesSerializer(serializers.ModelSerializer):
  class Meta:
    model = InvoiceLines
    fields = ['id','invoice','product','quantity','price_unit','price_total','users_id','sent','sent_date']
    read_only_fields = ['id','clients_id','users_id','created_at','modified_at','sent','sent_date','invoice_number','price_ati','price_vat','price_et','price_total',]