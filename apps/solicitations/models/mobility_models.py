from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from apps.solicitations.models.solicitation_models import Solicitation


class MobilitySheet(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="mobility_sheet")
    issue_date = models.DateField(null=True, blank=True)
    correlative = models.CharField(max_length=20, unique=True, null=True, blank=True)
    total_items = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Papeleta de salida - {self.solicitation.correlative}"


class MobilityItem(models.Model):
    TRANSPORT_CHOICES = [
        ('TAXI', 'Taxi'),
        ('BUS', 'Transporte colectivo'),
    ]
    mobility_sheet = models.ForeignKey(MobilitySheet, on_delete=models.CASCADE, related_name='expense_items')
    expense_date = models.DateField(null=True, blank=True)
    reason = models.CharField(max_length=150, null=True, blank=True)
    route = models.CharField(max_length=255, null=True, blank=True)
    transport = models.CharField(max_length=100, choices=TRANSPORT_CHOICES, null=True, blank=True)
    daily_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approver_signature = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.route} - {self.expense_date} - S/ {self.daily_amount}"

    def clean(self):
        total_for_day = \
            MobilityItem.objects.filter(expense_date=self.expense_date).aggregate(total=Sum('daily_amount'))[
                'total'] or 0
        if total_for_day + self.daily_amount > 42:
            raise ValidationError(
                f"No se puede gastar más de 42 soles en un solo día. El total actual para este día es S/ {total_for_day}.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
