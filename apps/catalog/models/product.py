from django.db import models
from django.urls import reverse
from django.contrib import admin

from apps.catalog.models import Label
from apps.catalog.models import Category

from apps.main.models import BaseModel
from apps.main.utils import uploder
from apps.main.mixins import SluginfyMixin


# Create your models here.
class ProductManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('label', 'category')
        return qs

    def available(self):
        qs = self.get_queryset()
        qs = qs.filter(available=True)
        return qs

    def available_with_images(self):
        qs = self.available()
        qs = qs.prefetch_related('images').all()
        return qs


class Product(SluginfyMixin, BaseModel):

    class Meta:
        db_table = 'products'
        ordering = ('created_at',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    objects: ProductManager = ProductManager()

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category,  on_delete=models.SET_NULL, null=True, blank=True)

    price = models.FloatField()
    old_price = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)

    image = models.ImageField(upload_to=uploder('products/thumbnails'), blank=True, null=True)

    available = models.BooleanField(default=True)

    description = models.TextField()

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={
            "pk": self.pk,
            "slug": self.slug
        })

    # def get_add_to_cart_url(self) :
    #     return reverse("stock:add-product-to-cart", kwargs={
    #         "pk" : self.pk
    #     })

    # def get_remove_from_cart_url(self) :
    #     return reverse("stock:remove-product-from-cart", kwargs={
    #         "pk" : self.pk
    #     })


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    source = models.ImageField(upload_to=uploder(
        'products/images'), blank=True, null=True)


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.key} : {self.value}'


# Admin
class ProductAdmin(admin.ModelAdmin):

    class ProductImageInline(admin.TabularInline):
        model = ProductImage

    class ProductAttributeInline(admin.TabularInline):
        model = ProductAttribute

    list_display = ('name', 'price', 'category', 'available')
    list_editable = ('available', )
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductAttributeInline]
