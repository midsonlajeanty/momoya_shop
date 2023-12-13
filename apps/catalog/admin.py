from django.contrib import admin

from .models import (
    Label, LabelAdmin,
    Product, ProductAdmin,
    Category, CategoryAdmin
)

# Register your models here.
admin.site.register(Label, LabelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
