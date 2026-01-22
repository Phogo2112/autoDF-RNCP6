from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    name_business = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Nom de l'entreprise"
    )
    siret = models.CharField(
        max_length=14,
        blank=True,
        default='',
        verbose_name="Numéro SIRET (14 chiffres)"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Adresse"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name="Ville"
    )
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        default='',
        verbose_name="Code postal"
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name="Téléphone mobile"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name="Téléphone mobile"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name="Ville"
    )
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        default='',
        verbose_name="Code postal"
    )

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    email = models.EmailField(unique=True)
    
    class Meta:
        db_table = 'user'
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.name_business} - {self.email}" if self.name_business else self.email
