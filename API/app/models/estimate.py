from django.db import models
from django.core.exceptions import ValidationError


class Estimate(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyé'),
        ('accepted', 'Accepté'),
        ('rejected', 'Refusé'),
        ('expired', 'Expiré')
    ]
    
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name='estimate',
        verbose_name="Créé par"
    )
    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name='estimate',
        verbose_name="Client"
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
        null=True,
        blank=True,
        default=0,
        verbose_name="Prix HT"
    )
    price_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name="TVA"
    )
    price_ati = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name="Prix TTC"
    )
    sent_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi"
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
        db_table = 'estimates'
        verbose_name = "Devis"
        verbose_name_plural = "Devis"
    
    def __str__(self):
        return f"Devis #{self.id} - {self.client} - {self.get_status_display()}"
    
    def is_editable(self):
        return self.status == 'draft'
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Estimate.objects.get(pk=self.pk)
            if not old_instance.is_editable():
                if self.status != old_instance.status:
                    super().save(update_fields=['status', 'modified_at'])
                    return
                raise ValidationError(
                    f"Ce devis ne peut plus être modifié (statut: {old_instance.get_status_display()})"
                )
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        if not self.is_editable():
            return
        
        lines = self.estimate_line.all()
        self.price_et = sum(line.amount_et or 0 for line in lines)
        self.price_vat = sum(line.calculate_vat() for line in lines)
        self.price_ati = self.price_et + self.price_vat
        self.save()
