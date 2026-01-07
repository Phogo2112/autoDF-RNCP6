"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MODÈLES autoDF - Architecture Multi-Tenant                 ║
║                                                                              ║
║  Ce fichier contient TOUS les modèles de l'application autoDF.              ║
║  Architecture : Chaque organisation (entreprise abonnée) a ses propres      ║
║  données isolées (clients, factures, devis).                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta


# ═══════════════════════════════════════════════════════════════════════════════
# 1. ORGANIZATION - Les entreprises qui s'abonnent à autoDF
# ═══════════════════════════════════════════════════════════════════════════════

class Organization(models.Model):
    """
    🏢 ORGANISATION = Une entreprise qui s'abonne à autoDF
    
    Pense à ça comme un "abonné Netflix", mais ici c'est une entreprise
    qui paie pour utiliser ton logiciel de facturation.
    
    Exemple : "Plomberie Martin SARL" est une Organization
    """
    
    # ─── Informations de l'entreprise ───
    company_name = models.CharField(
        max_length=200,
        verbose_name="Nom de l'entreprise",
        help_text="Nom commercial de l'entreprise abonnée"
    )
    
    siret = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="Numéro SIRET",
        help_text="14 chiffres obligatoires en France"
    )
    
    tva_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Numéro de TVA intracommunautaire",
        help_text="Format : FR12345678901"
    )
    
    # ─── Coordonnées ───
    email = models.EmailField(
        verbose_name="Email de contact"
    )
    
    phone = models.CharField(
        max_length=20,
        verbose_name="Téléphone"
    )
    
    address = models.CharField(
        max_length=255,
        verbose_name="Adresse"
    )
    
    postal_code = models.CharField(
        max_length=10,
        verbose_name="Code postal"
    )
    
    city = models.CharField(
        max_length=100,
        verbose_name="Ville"
    )
    
    country = models.CharField(
        max_length=100,
        default="France",
        verbose_name="Pays"
    )
    
    # ─── Logo pour personnaliser les factures ───
    logo = models.ImageField(
        upload_to='organizations/logos/',
        blank=True,
        null=True,
        verbose_name="Logo de l'entreprise",
        help_text="Apparaîtra sur les factures et devis"
    )
    
    # ─── Gestion de l'abonnement ───
    SUBSCRIPTION_PLANS = [
        ('free', 'Gratuit - 10 factures/mois'),
        ('pro', 'Pro - Factures illimitées'),
        ('enterprise', 'Enterprise - Factures illimitées + Support prioritaire'),
    ]
    
    subscription_plan = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_PLANS,
        default='free',
        verbose_name="Formule d'abonnement"
    )
    
    SUBSCRIPTION_STATUS = [
        ('trial', 'Période d\'essai'),
        ('active', 'Actif'),
        ('suspended', 'Suspendu (impayé)'),
        ('cancelled', 'Résilié'),
    ]
    
    subscription_status = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_STATUS,
        default='trial',
        verbose_name="Statut de l'abonnement"
    )
    
    subscription_start_date = models.DateField(
        auto_now_add=True,
        verbose_name="Date de début d'abonnement"
    )
    
    subscription_end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de fin d'abonnement",
        help_text="Uniquement si l'abonnement est résilié"
    )
    
    # ─── Métadonnées ───
    is_active = models.BooleanField(
        default=True,
        verbose_name="Organisation active"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} ({self.siret})"


# ═══════════════════════════════════════════════════════════════════════════════
# 2. USER - Les utilisateurs de chaque entreprise
# ═══════════════════════════════════════════════════════════════════════════════

class User(models.Model):
    """
    👤 USER = Une personne qui utilise autoDF DANS une entreprise
    
    Exemple : "Jean Martin" travaille chez "Plomberie Martin"
    → Jean est un User qui appartient à l'Organization "Plomberie Martin"
    
    ⚠️ IMPORTANT : Un User appartient à UNE SEULE Organization !
    """
    
    # ─── Lien avec l'organisation (CRUCIAL pour le multi-tenant) ───
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name="Organisation",
        help_text="L'entreprise à laquelle appartient cet utilisateur"
    )
    
    # ─── Informations personnelles ───
    firstname = models.CharField(
        max_length=100,
        verbose_name="Prénom"
    )
    
    lastname = models.CharField(
        max_length=100,
        verbose_name="Nom"
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Utilisé pour la connexion"
    )
    
    password = models.CharField(
        max_length=255,
        verbose_name="Mot de passe",
        help_text="Toujours stocké de manière sécurisée (hashé)"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )
    
    # ─── Rôles et permissions ───
    ROLES = [
        ('owner', 'Propriétaire - Tous les droits'),
        ('admin', 'Administrateur - Gestion complète'),
        ('user', 'Utilisateur - Création de factures uniquement'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='user',
        verbose_name="Rôle"
    )
    
    # ─── Statut ───
    is_active = models.BooleanField(
        default=True,
        verbose_name="Compte actif"
    )
    
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Dernière connexion"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['lastname', 'firstname']
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.organization.company_name})"
    
    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"


# ═══════════════════════════════════════════════════════════════════════════════
# 3. CLIENT - Les clients de chaque entreprise
# ═══════════════════════════════════════════════════════════════════════════════

class Client(models.Model):
    """
    🧑‍💼 CLIENT = Un client de l'entreprise (particulier OU entreprise)
    
    Exemple 1 (Particulier) : "Sophie Dubois" fait réparer sa plomberie
    Exemple 2 (Entreprise) : "Restaurant Le Gourmet SARL" commande des travaux
    
    ⚠️ IMPORTANT : Un Client appartient à UNE Organisation !
    Les clients de "Plomberie Martin" ne sont PAS visibles par "Électricité Dupont"
    """
    
    # ─── Lien avec l'organisation (CRUCIAL) ───
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name="Organisation"
    )
    
    # ─── Type de client ───
    CLIENT_TYPES = [
        ('particulier', 'Particulier'),
        ('entreprise', 'Entreprise'),
    ]
    
    type = models.CharField(
        max_length=20,
        choices=CLIENT_TYPES,
        verbose_name="Type de client"
    )
    
    # ─── Champs COMMUNS (particulier ET entreprise) ───
    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )
    
    address = models.CharField(
        max_length=255,
        verbose_name="Adresse"
    )
    
    postal_code = models.CharField(
        max_length=10,
        verbose_name="Code postal"
    )
    
    city = models.CharField(
        max_length=100,
        verbose_name="Ville"
    )
    
    country = models.CharField(
        max_length=100,
        default="France",
        verbose_name="Pays"
    )
    
    # ─── Champs PARTICULIER (nullable si type = 'entreprise') ───
    firstname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Prénom",
        help_text="Obligatoire si type = Particulier"
    )
    
    lastname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nom",
        help_text="Obligatoire si type = Particulier"
    )
    
    # ─── Champs ENTREPRISE (nullable si type = 'particulier') ───
    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Raison sociale",
        help_text="Obligatoire si type = Entreprise"
    )
    
    siret = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        verbose_name="Numéro SIRET",
        help_text="Obligatoire si type = Entreprise"
    )
    
    tva_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Numéro de TVA intracommunautaire"
    )
    
    # ─── Notes internes ───
    notes = models.TextField(
        blank=True,
        verbose_name="Notes internes",
        help_text="Informations importantes sur le client (non visibles sur les factures)"
    )
    
    # ─── Métadonnées ───
    is_active = models.BooleanField(
        default=True,
        verbose_name="Client actif"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-created_at']
        # Un client est unique par organisation (évite les doublons)
        unique_together = [['organization', 'email']]
    
    def __str__(self):
        if self.type == 'particulier':
            return f"{self.firstname} {self.lastname}"
        else:
            return self.company_name
    
    def clean(self):
        """
        🛡️ VALIDATION : Vérifie que les champs obligatoires sont remplis
        selon le type de client
        """
        if self.type == 'particulier':
            if not self.firstname or not self.lastname:
                raise ValidationError("Un particulier doit avoir un prénom et un nom")
        
        elif self.type == 'entreprise':
            if not self.company_name:
                raise ValidationError("Une entreprise doit avoir une raison sociale")
            if not self.siret:
                raise ValidationError("Une entreprise doit avoir un numéro SIRET")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. ESTIMATE - Les devis
# ═══════════════════════════════════════════════════════════════════════════════

class Estimate(models.Model):
    """
    📄 DEVIS = Proposition de prix envoyée au client
    
    Workflow :
    1. L'entrepreneur crée un devis
    2. Le client accepte / refuse
    3. Si accepté → peut être converti en facture
    
    Numérotation automatique : DEV-2025-001, DEV-2025-002...
    Repart à 001 chaque 1er janvier
    """
    
    # ─── Lien avec l'organisation ───
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='estimates',
        verbose_name="Organisation"
    )
    
    # ─── Numérotation automatique ───
    estimate_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro de devis",
        help_text="Format : DEV-2025-001"
    )
    
    year = models.IntegerField(
        verbose_name="Année",
        help_text="Permet la réinitialisation du compteur chaque 1er janvier"
    )
    
    # ─── Relations ───
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,  # Ne peut pas supprimer un client qui a des devis
        related_name='estimates',
        verbose_name="Client"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_estimates',
        verbose_name="Créé par"
    )
    
    # ─── Dates ───
    date = models.DateField(
        default=date.today,
        verbose_name="Date du devis"
    )
    
    validity_days = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        verbose_name="Validité (jours)",
        help_text="Nombre de jours pendant lesquels le devis est valable"
    )
    
    # ─── Statut ───
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyé au client'),
        ('accepted', 'Accepté'),
        ('refused', 'Refusé'),
        ('expired', 'Expiré'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Statut"
    )
    
    # ─── Montants ───
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Remise (%)",
        help_text="Remise globale appliquée sur le total HT"
    )
    
    total_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total HT (€)"
    )
    
    total_tva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total TVA (€)"
    )
    
    total_ttc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total TTC (€)"
    )
    
    # ─── Notes ───
    notes = models.TextField(
        blank=True,
        verbose_name="Notes / Conditions particulières",
        help_text="Apparaîtra sur le PDF du devis"
    )
    
    # ─── Conversion en facture ───
    converted_to_invoice = models.OneToOneField(
        'Invoice',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='source_estimate',
        verbose_name="Converti en facture"
    )
    
    # ─── PDF généré ───
    pdf_path = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Chemin du PDF",
        help_text="Chemin relatif vers le fichier PDF généré"
    )
    
    # ─── Métadonnées ───
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    class Meta:
        verbose_name = "Devis"
        verbose_name_plural = "Devis"
        ordering = ['-date', '-estimate_number']
        # Assure l'unicité du numéro par organisation et année
        unique_together = [['organization', 'year', 'estimate_number']]
    
    def __str__(self):
        return f"{self.estimate_number} - {self.client}"
    
    @property
    def validity_date(self):
        """Calcule la date d'expiration du devis"""
        return self.date + timedelta(days=self.validity_days)
    
    @property
    def is_expired(self):
        """Vérifie si le devis est expiré"""
        return date.today() > self.validity_date and self.status not in ['accepted', 'refused']
    
    def save(self, *args, **kwargs):
        """
        🔢 GÉNÉRATION AUTOMATIQUE DU NUMÉRO
        
        Si pas de numéro → génère automatiquement DEV-YYYY-XXX
        """
        if not self.estimate_number:
            self.year = date.today().year
            
            # Trouve le dernier numéro de l'année pour cette organisation
            last_estimate = Estimate.objects.filter(
                organization=self.organization,
                year=self.year
            ).order_by('-estimate_number').first()
            
            if last_estimate:
                # Extrait le numéro du format DEV-2025-042 → 042
                last_number = int(last_estimate.estimate_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            # Formate avec 3 chiffres : 1 → 001, 42 → 042
            self.estimate_number = f"DEV-{self.year}-{new_number:03d}"
        
        super().save(*args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# 5. ESTIMATE LINE - Les lignes de devis
# ═══════════════════════════════════════════════════════════════════════════════

class EstimateLine(models.Model):
    """
    📋 LIGNE DE DEVIS = Une prestation / un produit dans le devis
    
    Exemple :
    Devis DEV-2025-001
    ├─ Ligne 1 : Réparation fuite - 1 intervention - 150€ HT
    ├─ Ligne 2 : Remplacement joint - 2 unités - 25€ HT chacun
    └─ Ligne 3 : Déplacement - 1 forfait - 50€ HT
    """
    
    # ─── Lien avec le devis ───
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name="Devis"
    )
    
    # ─── Position d'affichage ───
    position = models.PositiveIntegerField(
        verbose_name="Position",
        help_text="Ordre d'affichage sur le PDF (1, 2, 3...)"
    )
    
    # ─── Description de la prestation ───
    description = models.CharField(
        max_length=500,
        verbose_name="Description",
        help_text="Ex: 'Réparation fuite d'eau salle de bain'"
    )
    
    # ─── Quantité ───
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Quantité"
    )
    
    unit = models.CharField(
        max_length=50,
        default="unité",
        verbose_name="Unité",
        help_text="Ex: 'jours', 'heures', 'unités', 'forfait'..."
    )
    
    # ─── Prix unitaire ───
    unit_price_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Prix unitaire HT (€)"
    )
    
    # ─── TVA ───
    tva_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux de TVA (%)",
        help_text="Ex: 20, 10, 5.5, 2.1"
    )
    
    # ─── Remise spécifique à cette ligne ───
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Remise ligne (%)"
    )
    
    # ─── Montants calculés ───
    total_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total HT (€)"
    )
    
    total_tva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total TVA (€)"
    )
    
    total_ttc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total TTC (€)"
    )
    
    class Meta:
        verbose_name = "Ligne de devis"
        verbose_name_plural = "Lignes de devis"
        ordering = ['estimate', 'position']
    
    def __str__(self):
        return f"{self.estimate.estimate_number} - Ligne {self.position}"
    
    def save(self, *args, **kwargs):
        """
        💰 CALCUL AUTOMATIQUE des montants
        
        total_ht = (quantity × unit_price_ht) - remise
        total_tva = total_ht × (tva_rate / 100)
        total_ttc = total_ht + total_tva
        """
        # Calcul du HT avec remise
        subtotal = self.quantity * self.unit_price_ht
        discount_amount = subtotal * (self.discount_percentage / 100)
        self.total_ht = subtotal - discount_amount
        
        # Calcul de la TVA
        self.total_tva = self.total_ht * (self.tva_rate / 100)
        
        # Calcul du TTC
        self.total_ttc = self.total_ht + self.total_tva
        
        super().save(*args, **kwargs)
        
        # 🔄 Met à jour les totaux du devis parent
        self.estimate.recalculate_totals()


# ═══════════════════════════════════════════════════════════════════════════════
# 6. INVOICE - Les factures
# ═══════════════════════════════════════════════════════════════════════════════

class Invoice(models.Model):
    """
    🧾 FACTURE = Document comptable officiel
    
    Peut être créée :
    - Depuis un devis accepté (conversion)
    - Directement (sans devis)
    
    Numérotation : FACT-2025-001, FACT-2025-002...
    """
    
    # ─── Lien avec l'organisation ───
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name="Organisation"
    )
    
    # ─── Numérotation automatique ───
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro de facture",
        help_text="Format : FACT-2025-001"
    )
    
    year = models.IntegerField(
        verbose_name="Année"
    )
    
    # ─── Relations ───
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='invoices',
        verbose_name="Client"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_invoices',
        verbose_name="Créé par"
    )
    
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='invoices',
        verbose_name="Devis source",
        help_text="Si cette facture provient d'un devis"
    )
    
    # ─── Dates ───
    date = models.DateField(
        default=date.today,
        verbose_name="Date de la facture"
    )
    
    due_date = models.DateField(
        verbose_name="Date d'échéance",
        help_text="Date limite de paiement"
    )
    
    # ─── Statut de la facture ───
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyée au client'),
        ('cancelled', 'Annulée'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Statut"
    )
    
    # ─── Statut du paiement ───
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('partial', 'Payé partiellement'),
        ('paid', 'Payé intégralement'),
        ('overdue', 'En retard'),
    ]
    
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="Statut de paiement"
    )
    
    # ─── Montants ───
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Remise (%)"
    )
    
    total_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total HT (€)"
    )
    
    total_tva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total TVA (€)"
    )
    
    total_ttc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total TTC (€)"
    )
    
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant payé (€)",
        help_text="Somme de tous les acomptes"
    )
    
    remaining_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Reste à payer (€)"
    )
    
    # ─── Notes ───
    notes = models.TextField(
        blank=True,
        verbose_name="Notes / Mentions",
        help_text="Ex: 'Travaux effectués avec succès', 'Client très satisfait'..."
    )
    
    # ─── PDF généré ───
    pdf_path = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Chemin du PDF"
    )
    
    # ─── Métadonnées ───
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-date', '-invoice_number']
        unique_together = [['organization', 'year', 'invoice_number']]
    
    def __str__(self):
        return f"{self.invoice_number} - {self.client}"
    
    @property
    def is_overdue(self):
        """Vérifie si la facture est en retard de paiement"""
        return (
            date.today() > self.due_date and 
            self.payment_status in ['pending', 'partial']
        )
    
    def save(self, *args, **kwargs):
        # Génération du numéro si nouveau
        if not self.invoice_number:
            self.year = date.today().year
            
            last_invoice = Invoice.objects.filter(
                organization=self.organization,
                year=self.year
            ).order_by('-invoice_number').first()
            
            if last_invoice:
                last_number = int(last_invoice.invoice_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.invoice_number = f"FACT-{self.year}-{new_number:03d}"
        
        # Calcul du reste à payer
        self.remaining_amount = self.total_ttc - self.paid_amount
        
        # Mise à jour automatique du statut de paiement
        if self.remaining_amount <= 0:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        elif self.is_overdue:
            self.payment_status = 'overdue'
        
        super().save(*args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# 7. INVOICE LINE - Les lignes de facture
# ═══════════════════════════════════════════════════════════════════════════════

class InvoiceLine(models.Model):

    # ─── Lien avec la facture ───
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name="Facture"
    )
    
    # ─── Position ───
    position = models.PositiveIntegerField(
        verbose_name="Position"
    )
    
    # ─── Description ───
    description = models.CharField(
        max_length=500,
        verbose_name="Description"
    )
    
    # ─── Quantité ───
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Quantité"
    )
    
    unit = models.CharField(
        max_length=50,
        default="unité",
        verbose_name="Unité"
    )
    
    # ─── Prix unitaire ───
    unit_price_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Prix unitaire HT (€)"
    )
    
    # ─── TVA ───
    tva_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux de TVA (%)"
    )
    
    # ─── Remise ───
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Remise ligne (%)"
    )
    
    # ─── Montants calculés ───
    total_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total HT (€)"
    )
    
    total_tva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total TVA (€)"
    )
    
    total_ttc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total TTC (€)"
    )
    
    # ─── Traçabilité ───
    added_after_estimate = models.BooleanField(
        default=False,
        verbose_name="Ajouté après le devis",
        help_text="True si cette ligne a été ajoutée APRÈS la conversion du devis"
    )
    
    note = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Note interne",
        help_text="Ex: 'Pièce découverte défectueuse sur place'"
    )
    
    class Meta:
        verbose_name = "Ligne de facture"
        verbose_name_plural = "Lignes de facture"
        ordering = ['invoice', 'position']
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - Ligne {self.position}"
    
    def save(self, *args, **kwargs):
        """💰 CALCUL AUTOMATIQUE des montants"""
        subtotal = self.quantity * self.unit_price_ht
        discount_amount = subtotal * (self.discount_percentage / 100)
        self.total_ht = subtotal - discount_amount
        
        self.total_tva = self.total_ht * (self.tva_rate / 100)
        self.total_ttc = self.total_ht + self.total_tva
        
        super().save(*args, **kwargs)
        
        # 🔄 Met à jour les totaux de la facture parent
        self.invoice.recalculate_totals()


# ═══════════════════════════════════════════════════════════════════════════════
# 8. PAYMENT - Les paiements (acomptes)
# ═══════════════════════════════════════════════════════════════════════════════

class Payment(models.Model):
    # ─── Lien avec la facture ───
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Facture"
    )
    
    # ─── Date et montant ───
    payment_date = models.DateField(
        default=date.today,
        verbose_name="Date du paiement"
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Montant (€)"
    )
    
    # ─── Moyen de paiement ───
    PAYMENT_METHODS = [
        ('cash', 'Espèces'),
        ('check', 'Chèque'),
        ('transfer', 'Virement'),
        ('card', 'Carte bancaire'),
        ('other', 'Autre'),
    ]
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name="Moyen de paiement"
    )
    
    # ─── Référence ───
    reference = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Référence",
        help_text="Ex: numéro de chèque, référence de virement..."
    )
    
    # ─── Notes ───
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    
    # ─── Traçabilité ───
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Enregistré par"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'enregistrement"
    )
    
    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.amount}€ le {self.payment_date}"
    
    def save(self, *args, **kwargs):
        """
        💰 Met à jour automatiquement le montant payé de la facture
        """
        super().save(*args, **kwargs)
        
        # Recalcule le total payé sur la facture
        total_paid = self.invoice.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        self.invoice.paid_amount = total_paid
        self.invoice.save()


# ═══════════════════════════════════════════════════════════════════════════════
# MÉTHODES UTILITAIRES AJOUTÉES AUX MODÈLES
# ═══════════════════════════════════════════════════════════════════════════════

def recalculate_totals(self):
    """
    🔄 Recalcule les totaux d'un devis ou d'une facture
    À appeler après modification des lignes
    """
    lines = self.lines.all()
    
    self.total_ht = sum(line.total_ht for line in lines)
    self.total_tva = sum(line.total_tva for line in lines)
    self.total_ttc = sum(line.total_ttc for line in lines)
    
    # Applique la remise globale si présente
    if self.discount_percentage > 0:
        discount = self.total_ht * (self.discount_percentage / 100)
        self.total_ht -= discount
        self.total_ttc = self.total_ht + self.total_tva
    
    self.save()

# Ajoute cette méthode aux modèles Estimate et Invoice
Estimate.recalculate_totals = recalculate_totals
Invoice.recalculate_totals = recalculate_totals