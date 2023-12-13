from django.contrib import admin

from .models import (
    ShippingMethod, ShippingMethodAdmin,
    Shipping, ShippingAdmin
)

admin.site.register(Shipping, ShippingAdmin)
admin.site.register(ShippingMethod, ShippingMethodAdmin)
