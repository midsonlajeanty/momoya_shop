from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator

from apps.main.utils import random_string

from apps.main.models import BaseModel
from apps.sales.models import Order

# HELPERS
class ProcessingTimeValidator(RegexValidator):
    regex = r'^\d+-\d+$'
    message = 'Processing time must be in format: "integer-integer'

# HELPERS
def generate_traking_reference():
    ref = random_string(8).upper()
    if Shipping.objects.filter(traking_number=ref).exists():
        return generate_traking_reference()
    return ref

class ShippingMethodManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(available=True)
        return qs

class ShippingMethod(BaseModel):

    class Meta:
        ordering = ['-default', '-created_at']

    name = models.CharField(max_length=255)
    description = models.TextField()
    processing_time = models.CharField(max_length=10, validators=[ProcessingTimeValidator], blank=True, null=True)
    address_required = models.BooleanField(default=False)
    price = models.FloatField()
    available = models.BooleanField(default=True)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.available and self.default:
            raise ValueError('Default shipping method must be available')
        if self.default:
            ShippingMethod.objects.filter(default=True).update(default=False)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

# SHIPPING
class ShipingManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('method', 'address')
        return qs
    
    def with_order(self):
        qs = self.get_queryset()
        qs = qs.select_related('order')
        return qs

class Shipping(BaseModel):

    objects: ShipingManager = ShipingManager()

    traking_number =  models.CharField(max_length=12, unique=True, db_index=True, default=generate_traking_reference)
    method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, related_name='shipping', on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.method} - #{self.traking_number}'
    
    @property
    def name(self):
        return self.method.name
    
    @property
    def cost(self):
        return self.method.price
    
    @property
    def processing_time(self):
        return f'{self.method.processing_time} days'
    
    @property
    def shipping_address(self):
        if not hasattr(self, 'address'):
            return None
        return self.address.address
    
    @property
    def full_address(self):
        if not hasattr(self, 'address'):
            return None
        return str(self.address)
    

class ShippingAddress(BaseModel):
    shipping = models.OneToOneField(Shipping, related_name='address', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{5}(?:-\d{4})?$')])
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.zipcode}, {self.country}"
    


#  MODEL ADMIN
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'processing_time']


class ShippingAdmin(admin.ModelAdmin):
    
    class ShippingAddressInline(admin.TabularInline):
        model = ShippingAddress
        extra = 0

    list_display = ['traking_number', 'method', 'cost', 'processing_time']
    inlines = [ShippingAddressInline]


    
