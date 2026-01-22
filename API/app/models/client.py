from django.db import models

class Client(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('individuals', 'Particulier'),
        ('business', 'Entreprise')
    ]
    
    client_type = models.CharField(
        max_length=20,
        choices=CLIENT_TYPE_CHOICES,
        verbose_name="Type de client"
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name='client',
        verbose_name="Créé par"
    )
    email = models.EmailField(
        verbose_name="Email"
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name="Téléphone mobile"
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Adresse"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Ville"
    )
    postal_code = models.CharField(
        max_length=10,
        verbose_name="Code postal"
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Prénom (particulier)"
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Nom (particulier)"
    )
    name_organisation = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Nom de l'entreprise"
    )
    siret = models.CharField(
        max_length=14,
        blank=True,
        default='',
        verbose_name="Numéro SIRET (entreprise)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    class Meta:
        db_table = 'client'
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    
    def __str__(self):
        if self.client_type == 'individuals':
            return f"{self.first_name} {self.last_name}"
        return f"{self.name_organisation}"
