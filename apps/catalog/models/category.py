from django.db import models
from django.urls import reverse
from django.contrib.admin import ModelAdmin

from apps.main.models import BaseModel
from apps.main.mixins import SluginfyMixin


# Create your models here.
class Category(SluginfyMixin, BaseModel):

    class Meta:
        db_table = 'categories'
        ordering = ('created_at',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalogue:category", kwargs={
            "pk": self.pk,
            "slug": self.slug
        })


class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}