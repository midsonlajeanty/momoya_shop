from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.admin import ModelAdmin
from django.db.models.signals import post_migrate

from apps.main.models import BaseModel
from apps.main.mixins import SluginfyMixin


# Create your models here.
class Label(SluginfyMixin, BaseModel) :

    class Meta:
        db_table = 'labels'
        ordering = ('created_at',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) :
        return self.name
     
    def get_absolute_url(self) :
        return reverse("catalog:label", kwargs={
            "pk": self.pk,
            "slug" : self.slug
        })


class LabelAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

