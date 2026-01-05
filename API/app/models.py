from datetime import date
from django.db import models
from django.contrib.auth.hashers import make_password
from typing import Any, cast

# Create your models here.


class Estimate(models.Model):
  date = models.DateField()
  firstname = models.CharField(max_length=100)
  
  def __str__(self):
      return self.firstname

class Statistics(models.Model):
  price_ht = models.FloatField()
  price_tva = models.FloatField()
  price_ttc = models.FloatField()


class User(models.Model):
  lastname = models.CharField(max_length=25)
  firstname = models.CharField(max_length=25)
  password = models.CharField(max_length=50)
  birthday = models.DateField()
  email = models.EmailField()
  domaine = models.CharField(max_length=100)
  number_phone = models.CharField(max_length=20)

class Invoice(models.Model):
  date = models.DateField()
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)
  departement_number = models.IntegerField()
    
