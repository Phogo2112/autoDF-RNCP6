from django.db import models

class InvoiceLine(models.Model):
    LINES_TYPE_CHOICES = [
        ('benefit', 'Prestation'),
        ('supply', 'Fourniture')
    ]
    
    invoice = models.ForeignKey(
        "Invoice",
        on_delete=models.CASCADE,
        related_name='invoice_line',
        verbose_name="Facture"
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name="Description"
    )
    line_type = models.CharField(
        max_length=20,
        choices=LINES_TYPE_CHOICES,
        blank=True,
        default='benefit',
        verbose_name="Type de ligne"
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name="Quantité"
    )
    price_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Prix unitaire"
    )
    taux_vat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20.0,
        verbose_name="Taux de TVA (%)"
    )
    amount_et = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant HT"
    )
    note = models.TextField(
        blank=True,
        default='',
        verbose_name="Note"
    )
    
    class Meta:
        db_table = 'invoice_lines'
        verbose_name = "Ligne de facture"
        verbose_name_plural = "Lignes de facture"
    
    def __str__(self):
        return f"{self.description[:50]} - {self.amount_et}€"
    
    def save(self, *args, **kwargs):
        if not self.invoice.is_editable():
            raise ValidationError(
                f"Cette facture ne peut plus être modifiée (statut: {self.invoice.get_status_display()})"
            )
        if self.quantity and self.price_unit:
            self.amount_et = Decimal(str(self.quantity)) * self.price_unit
        
        super().save(*args, **kwargs)
        
        self.invoice.calculate_totals()
    
    def delete(self, *args, **kwargs):
        if not self.invoice.is_editable():
            raise ValidationError(
                f"Cette ligne ne peut plus être supprimée (facture {self.invoice.get_status_display()})"
            )
        super().delete(*args, **kwargs)
        self.invoice.calculate_totals()
    
    def calculate_vat(self):
        if self.amount_et and self.taux_vat:
            return self.amount_et * (self.taux_vat / Decimal('100'))
        return Decimal('0.00')