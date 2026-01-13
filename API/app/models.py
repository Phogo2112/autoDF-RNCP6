
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal
from datetime import date


class Users(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Email de connexion"
    )
    name_business = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Nom de l'entreprise"
    )
    password = models.CharField(
        max_length=255,
        verbose_name="Mot de passe (hashé)"
    )
    
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Prénom"
    )
    
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Nom"
    )
    
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Timestamp de modification"
    )
    
    last_login = models.DateField(
        null=True,
        blank=True,
        verbose_name="Dernière connexion"
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def set_password(self, raw_password):
        """Hash le mot de passe avant de le sauvegarder"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Vérifie si le mot de passe est correct"""
        return check_password(raw_password, self.password)


class Clients(models.Model):
    
    CLIENTS_TYPE_CHOICES = [
        ('individuals', 'Particulier'),
        ('business', 'Entreprise')
    ]
    
    siret = models.CharField(
        max_length=14,
        verbose_name="Numéro SIRET 14 chiffres",
        blank=True,
        null=True
    )
    
    clients_type = models.CharField(
        max_length=255,
        choices=CLIENTS_TYPE_CHOICES,
        verbose_name="Type de client"
    )
    
    name = models.CharField(
        max_length=255,
        verbose_name="Nom ou raison sociale"
    )
    
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True, default="",
        verbose_name="Prénom"
    )
    
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True, default="",
        verbose_name="Nom de famille"
    )
    
    address = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Adresse"
    )
    
    postal_code = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        verbose_name="Code postal"
    )
    
    email = models.EmailField(
        blank=False,
        null=False,
        verbose_name="Email"
    )
    
    mobile = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Téléphone mobile"
    )
    
    users = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        db_column='users_id',
        related_name='clients',
        blank=False,
        null=False
    )
    
    created_at = models.DateField(
        auto_now_add=True,
        blank=False,
        null=False,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateField(
        auto_now=True,
        blank=False,
        null=False,
        verbose_name="Date de modification"
    )
    
    class Meta:
        db_table = 'clients'
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    
    def __str__(self):
        if self.client_type == 'individuals':
            return f"{self.first_name} {self.last_name}"
        return f"{self.name} (SIRET: {self.siret})"


class Estimates(models.Model):
    
    users = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        db_column='users_id',
        related_name='estimates',
        verbose_name=f"Créé par {Users.id}"
    )
    
    clients = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        db_column='clients_id',
        related_name='estimates',
        verbose_name="Client"
    )
    
    price_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix HT (ET = Excluding Tax)"
    )
    
    price_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="TVA (VAT)"
    )
    
    price_ati = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix TTC (ATI = All Taxes Included)"
    )
    
    sent = models.BooleanField(
        default=False,
        blank=False,
        null=False,
        verbose_name="Envoyé au client ?"
    )
    
    sent_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi"
    )
    
    created_at = models.DateField(
        auto_now_add=True,
        blank=False,
        null=False,
        verbose_name="Date de création"
    )
    
    modified_at = models.DateField(
        auto_now=True,
        blank=False,
        null=False,
        verbose_name="Date de modification"
    )
    
    created_by = models.DateField(
        null=True,
        blank=True,
    )
    
    class Meta:
        db_table = 'estimates'
        verbose_name = "Devis"
        verbose_name_plural = "Devis"
    
    def __str__(self):
        return f"Devis #{self.id} - {self.clients} - {self.price_ati}€"
    
    def calculate_totals(self):
        lines = self.estimate_lines.all()
        
        self.price_et = sum(line.amount_et or 0 for line in lines)
        self.price_vat = sum(line.calculate_vat() for line in lines)
        self.price_ati = self.price_et + self.price_vat
        
        self.save()


class EstimateLines(models.Model):
    
    LINES_TYPE_CHOICES = [
        ('benefit', 'Prestation'),
        ('supply', 'Fourniture')
    ]
    
    estimates = models.ForeignKey(
        Estimates,
        on_delete=models.CASCADE,
        db_column='estimates_id',
        related_name='estimate_lines',
        verbose_name="Devis"
    )
    
    description = models.TextField(
        blank = True, default='',
        null = True,
        verbose_name="Description"
    )
    
    line_type = models.CharField(
        max_length=255,
        choices=LINES_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Type de ligne"
    )
    
    quantity = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Quantité"
    )
    
    price_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix unitaire"
    )
    
    rate_vat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Taux de TVA (%)"
    )
    
    amount_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant HT"
    )
    
    note = models.CharField(
        max_length=255,
        blank=True,
        default='',
        null=True,
        verbose_name="Note"
    )
    
    class Meta:
        db_table = 'estimate_lines'
        verbose_name = "Ligne de devis"
        verbose_name_plural = "Lignes de devis"
    
    def __str__(self):
        return f"{self.description} - {self.amount_et}€"
    
    def save(self, *args, **kwargs):

        if self.quantity and self.unit_prix:
            self.amount_et = Decimal(str(self.quantity)) * self.unit_prix
        super().save(*args, **kwargs)
        
        self.estimates.calculate_totals()
    
    def calculate_vat(self):
        if self.amount_et and self.rate_vat:
            return self.amount_et * (self.rate_vat / Decimal('100'))
        return Decimal('0.00')


class Invoices(models.Model):
    
    PAYMENTS_METHOD_CHOICES = [
        ('CB', 'Carte Bancaire'),
        ('Virement', 'Virement'),
        ('espèce', 'Espèces')
    ]
    
    invoice_number = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Numéro de facture"
    )
    
    clients = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        db_column='clients_id',
        related_name='invoices',
        verbose_name="Client"
    )
    
    users = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        db_column='users_id',
        related_name='invoices',
        verbose_name="Créé par"
    )
    
    price_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name="Prix HT"
    )
    
    price_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name="TVA"
    )
    
    price_ati = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name="Prix TTC"
    )
    
    sent = models.BooleanField(
        default=False,
        verbose_name="Envoyé au client ?"
    )
    
    sent_date = models.DateField(
        null=False,
        blank=False,
        verbose_name="Date d'envoi"
    )
    
    payements_method = models.CharField(
        max_length=255,
        choices=PAYMENTS_METHOD_CHOICES,
        blank=False,
        null=False,
        verbose_name="Mode de paiement"
    )
    
    payment_date = models.DateField(
        null=False,
        blank=False,
        verbose_name="Date de paiement"
    )
    
    created_at = models.DateField(
        auto_now_add=True,
        blank=False,
        null=False,
        verbose_name="Date de création"
    )
    
    modified_at = models.DateField(
        auto_now=True,
        blank=False,
        null=False,
        verbose_name="Date de modification"
    )
    
    class Meta:
        db_table = 'invoices'
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
    
    def __str__(self):
        return f"{self.invoice_number} - {self.clients} - {self.price_ati}€"
    
    def calculate_totals(self):
        lines = self.invoice_lines.all()
        
        self.price_et = sum(line.amount_et or 0 for line in lines)
        self.price_vat = sum(line.calculate_vat() for line in lines)
        self.price_ati = self.price_et + self.price_vat
        
        self.save()


class InvoiceLines(models.Model):
    LINES_TYPE_CHOICES = [
        ('benefit', 'Prestation'),
        ('supply', 'Fourniture')
    ]
    
    invoice = models.ForeignKey(
        Invoices,
        on_delete=models.CASCADE,
        db_column='invoice_id',
        related_name='invoice_lines',
        verbose_name="Facture"
    )
    
    description = models.TextField(
        blank=True, default='',
        null=True,
        verbose_name="Description"
    )
    
    line_type = models.CharField(
        max_length=255,
        choices=LINES_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Type de ligne"
    )
    
    quantity = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Quantité"
    )
    
    price_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix unitaire"
    )
    
    taux_vat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Taux de TVA (%)"
    )
    
    amount_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant HT"
    )
    
    note = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Note"
    )
    
    class Meta:
        db_table = 'invoice_lines'
        verbose_name = "Ligne de facture"
        verbose_name_plural = "Lignes de facture"
    
    def __str__(self):
        return f"{self.description} - {self.amount_et}€"
    
    def save(self, *args, **kwargs):
        if self.quantity and self.price_unit:
            self.amount_et = Decimal(str(self.quantity)) * self.price_unit
        super().save(*args, **kwargs)

        self.invoice.calculate_totals()
    
    def calculate_vat(self):
        if self.amount_et and self.taux_vat:
            return self.amount_et * (self.taux_vat / Decimal('100'))
        return Decimal('0.00')