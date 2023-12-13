from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin

from apps.main.models import BaseModel

UserModel = get_user_model()

class User(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Address(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.zipcode}, {self.country}"


class Guest(BaseModel):

    class Meta:
        ordering = ['-created_at']
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.name



class UserAdmin(AbstractUserAdmin):

    class AddressInline(admin.TabularInline):
        model = Address
        extra = 0
    
    inlines = [AddressInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']