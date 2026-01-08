

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal
from datetime import date


class User(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Email de connexion"
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


class Client(models.Model):
    
    CLIENT_TYPE_CHOICES = [
        ('individuals', 'Particulier'),
        ('business', 'Entreprise')
    ]
    
    SIRET_TYPE_CHOICES = [
        ('individuals', 'Particulier'),
        ('business', 'Entreprise')
    ]
    
    # --- Type de client ---
    client_type = models.CharField(
        max_length=255,
        choices=CLIENT_TYPE_CHOICES,
        verbose_name="Type de client"
    )
    
    # --- Nom (pour particulier ou entreprise) ---
    name = models.CharField(
        max_length=255,
        verbose_name="Nom ou raison sociale"
    )
    
    # --- Pour les particuliers ---
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
        verbose_name="Nom de famille"
    )
    
    # --- Pour les entreprises ---
    siret_type = models.CharField(
        max_length=255,
        choices=SIRET_TYPE_CHOICES,
        verbose_name="Type de SIRET"
    )
    
    siret = models.CharField(
        max_length=14,
        verbose_name="Numéro SIRET",
        help_text="14 caractères - Ex: 12345678901234"
    )
    
    # --- Coordonnées ---
    address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Adresse"
    )
    
    postal_code = models.CharField(
        max_length=10,
        verbose_name="Code postal"
    )
    
    email = models.EmailField(
        verbose_name="Email"
    )
    
    mobile = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Téléphone mobile"
    )
    
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='users_id',
        related_name='clients'
    )
    
    # --- Dates ---
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateField(
        auto_now=True,
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


class Estimate(models.Model):
    
    # --- Liens ---
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='users_id',
        related_name='estimates',
        verbose_name="Créé par"
    )
    
    clients = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        db_column='clients_id',
        related_name='estimates',
        verbose_name="Client"
    )
    
    # --- Montants ---
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
    
    # --- Envoi ---
    sent = models.BooleanField(
        default=False,
        verbose_name="Envoyé au client ?"
    )
    
    sent_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi"
    )
    
    # --- Dates ---
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    modified_at = models.DateField(
        auto_now=True,
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
        """Recalcule les totaux à partir des lignes"""
        lines = self.estimate_lines.all()
        
        self.price_et = sum(line.amount_et or 0 for line in lines)
        self.price_vat = sum(line.calculate_vat() for line in lines)
        self.price_ati = self.price_et + self.price_vat
        
        self.save()


class EstimateLine(models.Model):
    
    LINE_TYPE_CHOICES = [
        ('benefit', 'Prestation'),
        ('supply', 'Fourniture')
    ]
    
    # --- Lien avec le devis ---
    estimates = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE,
        db_column='estimates_id',
        related_name='estimate_lines',
        verbose_name="Devis"
    )
    
    # --- Description ---
    description = models.CharField(
        max_length=255,
        verbose_name="Description"
    )
    
    # --- Type de ligne ---
    line_type = models.CharField(
        max_length=255,
        choices=LINE_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Type de ligne"
    )
    
    # --- Quantité et prix ---
    quantity = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Quantité"
    )
    
    unit_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix unitaire"
    )
    
    # --- TVA ---
    rate_vat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Taux de TVA (%)"
    )
    
    # --- Montant ---
    amount_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant HT"
    )
    
    # --- Note optionnelle ---
    note = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Note"
    )
    
    class Meta:
        db_table = 'estimate_lines'
        verbose_name = "Ligne de devis"
        verbose_name_plural = "Lignes de devis"
    
    def __str__(self):
        return f"{self.description} - {self.amount_et}€"
    
    def save(self, *args, **kwargs):
        """Calcule le montant HT avant de sauvegarder"""
        if self.quantity and self.unit_prix:
            self.amount_et = Decimal(str(self.quantity)) * self.unit_prix
        super().save(*args, **kwargs)
        
        # Recalcule les totaux du devis parent
        self.estimates.calculate_totals()
    
    def calculate_vat(self):
        """Calcule le montant de TVA"""
        if self.amount_et and self.rate_vat:
            return self.amount_et * (self.rate_vat / Decimal('100'))
        return Decimal('0.00')


class Invoice(models.Model):
    
    PAYMENT_METHOD_CHOICES = [
        ('CB', 'Carte Bancaire'),
        ('Virement', 'Virement'),
        ('espèce', 'Espèces')
    ]
    
    # --- Numéro de facture ---
    invoice_number = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Numéro de facture"
    )
    
    # --- Liens ---
    clients = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        db_column='clients_id',
        related_name='invoices',
        verbose_name="Client"
    )
    
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='users_id',
        related_name='invoices',
        verbose_name="Créé par"
    )
    
    # --- Montants ---
    price_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix HT"
    )
    
    price_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="TVA"
    )
    
    price_ati = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix TTC"
    )
    
    # --- Envoi ---
    sent = models.BooleanField(
        default=False,
        verbose_name="Envoyé au client ?"
    )
    
    sent_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi"
    )
    
    # --- Paiement ---
    payements_method = models.CharField(
        max_length=255,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Mode de paiement"
    )
    
    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de paiement"
    )
    
    # --- Dates ---
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    modified_at = models.DateField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    class Meta:
        db_table = 'invoices'
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
    
    def __str__(self):
        return f"{self.invoice_number} - {self.clients} - {self.price_ati}€"
    
    def calculate_totals(self):
        """Recalcule les totaux à partir des lignes"""
        lines = self.invoice_lines.all()
        
        self.price_et = sum(line.amount_et or 0 for line in lines)
        self.price_vat = sum(line.calculate_vat() for line in lines)
        self.price_ati = self.price_et + self.price_vat
        
        self.save()


class InvoiceLine(models.Model):
    LINE_TYPE_CHOICES = [
        ('benefit', 'Prestation'),
        ('supply', 'Fourniture')
    ]
    
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        db_column='invoice_id',
        related_name='invoice_lines',
        verbose_name="Facture"
    )
    
    # --- Description ---
    description = models.CharField(
        max_length=255,
        verbose_name="Description"
    )
    
    # --- Type de ligne ---
    line_type = models.CharField(
        max_length=255,
        choices=LINE_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Type de ligne"
    )
    
    # --- Quantité et prix ---
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
    
    # --- TVA ---
    taux_vat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Taux de TVA (%)"
    )
    
    # --- Montant ---
    amount_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant HT"
    )
    
    # --- Note optionnelle ---
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
        
        # Recalcule les totaux de la facture parent
        self.invoice.calculate_totals()
    
    def calculate_vat(self):
        if self.amount_et and self.taux_vat:
            return self.amount_et * (self.taux_vat / Decimal('100'))
        return Decimal('0.00')


