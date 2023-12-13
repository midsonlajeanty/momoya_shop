from django.db import models
from django.contrib import admin

from apps.main.models import BaseModel
from apps.main.utils import random_string

from .order import Order

# CHOICES
PAYMENT_STATUS = (
    ('PENDING', 'Pending'),
    ('COMPLETED', 'Completed'),
    ('FAILED', 'Failed'),
    ('CANCELLED', 'Cancelled'),
)

# HELPERS
def generate_payment_reference():
    ref = random_string(8).upper()
    if Payment.objects.filter(reference=ref).exists():
        return generate_payment_reference()
    return ref


class PaymentMethod(BaseModel):

    class Meta:
        ordering = ['default', '-created_at']

    name = models.CharField(max_length=255, unique=True)
    alias = models.CharField(editable=False, max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs) -> None:
        if not self.available and self.default:
            raise ValueError('Default payment method must be available')
         
        if self.default:
            PaymentMethod.objects.filter(default=True).update(default=False)

        if not self.alias:
            self.alias = self.name.upper().replace(' ', '_')
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class PaymentManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('method')
        return qs
    
    def with_order(self):
        qs = self.get_queryset()
        qs = qs.select_related('order')
        return qs

class Payment(BaseModel):

    objects: PaymentManager = PaymentManager()

    reference = models.CharField(max_length=12, unique=True, db_index=True, default=generate_payment_reference)
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.RESTRICT)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.method} - {self.amount}'
    
    @property
    def name(self):
        return self.method.name
    

# MODEL ADMIN
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'alias', 'description']
    readonly_fields = ['alias']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'order', 'method', 'amount', 'status']
    readonly_fields = ['reference', 'order', 'method', 'amount', 'status', 'details']
