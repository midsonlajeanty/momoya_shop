from django.contrib import admin
from django.contrib.auth.models import Group

from apps.account.models import (
    User, UserAdmin,
    Guest, GuestAdmin
)


# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Guest, GuestAdmin)