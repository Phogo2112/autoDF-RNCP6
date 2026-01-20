from django.db import models

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyée'),
        ('paid', 'Payée'),
        ('cancelled', 'Annulée')
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('CB', 'Carte Bancaire'),
        ('Virement', 'Virement'),
        ('Espece', 'Espèces'),
        ('Cheque', 'Chèque')
    ]
    
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro de facture"
    )
    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name='invoice',
        verbose_name="Client"
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name='invoice',
        verbose_name="Créé par"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Statut"
    )
    price_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Prix HT"
    )
    price_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="TVA"
    )
    price_ati = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Prix TTC"
    )
    sent_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi"
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        default='',
        verbose_name="Mode de paiement"
    )
    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de paiement"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    class Meta:
        db_table = 'invoices'
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
    
    def __str__(self):
        return f"{self.invoice_number} - {self.clients} - {self.get_status_display()}"
    
    def is_editable(self):
        return self.status == 'draft'
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Invoices.objects.get(pk=self.pk)
            if not old_instance.is_editable():
                if self.status != old_instance.status:
                    super().save(update_fields=['status', 'modified_at'])
                    return
                raise ValidationError(
                    f"Cette facture ne peut plus être modifiée (statut: {old_instance.get_status_display()})"
                )
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        if not self.is_editable():
            return
        
        lines = self.invoice_lines.all()
        self.price_et = sum(line.amount_et or 0 for line in lines)
        self.price_vat = sum(line.calculate_vat() for line in lines)
        self.price_ati = self.price_et + self.price_vat
        self.save()

