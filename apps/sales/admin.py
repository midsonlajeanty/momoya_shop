from django.contrib import admin

from .models import (
    Order, OrderAdmin,
    PaymentMethod, PaymentMethodAdmin,
    Payment, PaymentAdmin,
)

admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Payment, PaymentAdmin)


