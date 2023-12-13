from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.main.models import BaseModel
from apps.main.utils import random_string

from apps.catalog.models import Product
from apps.account.models import Guest

UserModel = get_user_model()


# CHOICES
ORDER_CREATOR_TYPE = (
    ('GUEST', 'Guest'),
    ('USER', 'User'),
)

ORDER_STATUS = (
    ('CREATED', 'Created'),
    ('PENDING', 'Pending'),
    ('SHIPPED', 'Shipped'),
    ('RETURNED', 'Returned'),
    ('REFUNDED', 'Refunded'),
    ('CANCELLED', 'Cancelled'),
)

# HELPERS
def generate_reference():
    ref = random_string(8).upper()
    if Order.objects.filter(reference=ref).exists():
        return generate_reference()
    return ref


# ORDER
class OrderManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('user', 'guest', 'shipping')
        return qs

    def with_items(self):
        qs = self.get_queryset()
        qs = qs.prefetch_related('items').all()
        return qs

class Order(BaseModel):

    class Meta:
        ordering = ['-created_at']

    objects: OrderManager = OrderManager()

    reference = models.CharField( max_length=12, unique=True, db_index=True, default=generate_reference)
    creator_type = models.CharField(max_length=20, choices=ORDER_CREATOR_TYPE, default='GUEST')
    guest = models.ForeignKey(Guest, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(UserModel, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)

    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='CREATED')

    @property
    def total(self):
        items_price = sum(item.cost for item in self.items.all())
        if hasattr(self, 'shipping'):
            return self.shipping.cost + items_price
        return items_price

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_unique_items(self):
        return self.items.count()

    @property
    def creator(self):
        if self.creator_type == 'GUEST':
            return self.guest
        return self.user

    @property 
    def get_checkout_url(self):
        return reverse("sales:checkout", kwargs={
            "pk": self.pk,
            "reference": self.reference
        })
    
    @property 
    def get_process_checkout_url(self):
        return reverse("sales:process_checkout", kwargs={
            "pk": self.pk,
            "reference": self.reference
        })
    
    @property 
    def get_payment_url(self):
        return reverse("sales:payment", kwargs={
            "pk": self.pk,
            "reference": self.reference
        })

    def save(self, *args, **kwargs) -> None:
        if self.status != 'CREATED':
            if self.creator_type == 'GUEST' and not self.guest:
                raise ValueError('Guest is required')
            if self.creator_type == 'USER' and not self.user:
                raise ValueError('User is required')
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Order #{self.reference}"


# ORDER ITEM
class OrderItemManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('product')
        return qs

class OrderItem(BaseModel):

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_order_item'
            )
        ]

    objects: OrderItemManager = OrderItemManager()

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.RESTRICT)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)

    @property
    def cost(self):
        return self.price * self.quantity

    @property
    def name(self):
        return self.product.name

    @property
    def image(self):
        return self.product.image.url

    @property
    def description(self):
        return self.product.description
    
    @property
    def get_absolute_url(self):
        return self.product.get_absolute_url


    def __str__(self):
        return f'{self.order.reference} - {self.product.name}'



# MODEL ADMIN
class OrderAdmin(admin.ModelAdmin):

    class OrderItemInline(admin.TabularInline):
        model = OrderItem
        extra = 0

    list_display = ['reference', 'status', 'total', 'creator_type']
    inlines = [OrderItemInline]