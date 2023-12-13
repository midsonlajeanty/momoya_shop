from typing import Any
from django.db import transaction
from django.http import HttpRequest
from django.views.generic import DetailView
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.catalog.models import Product
from apps.sales.models import OrderItem, Order
from apps.delivery.models import ShippingMethod, Shipping

from apps.sales.forms import OrderCreateForm
from apps.account.forms import GuestForm
from apps.delivery.forms import ShippingAddressForm


@require_POST
def create_order(request: HttpRequest):
    form = OrderCreateForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        print(cd)

        product: Product = get_object_or_404(Product, id=cd['product_id'])

        # Ceate Order
        order: Order = Order.objects.create()

        # Create OrderItem
        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=cd['quantity']
        )

        return redirect(order.get_checkout_url)
    
    return redirect(product.get_absolute_url)


class CheckoutView(DetailView):
    template_name = 'sales/checkout.html'
    queryset = Order.objects.with_items()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['shipping_methods'] = ShippingMethod.objects.all()
        context['shipping_address_form'] = ShippingAddressForm()
        context['guest_form'] = GuestForm()
        return context


@require_POST
def process_checkout(request: HttpRequest, pk: int, reference: str):
    order: Order = get_object_or_404(Order, id=pk, reference=reference)

    guest_form = GuestForm(request.POST)
    shipping_address_form = ShippingAddressForm(request.POST)
    shipping_method = ShippingMethod.objects.get(pk=request.POST.get('shipping_method_id'))

    with transaction.atomic():
        # Create Shipping
        shipping = Shipping.objects.create(
            order=order,
            method=shipping_method,
        )

        # Create Shipping Address
        if shipping_method.address_required:
            if shipping_address_form.is_valid():
                shipping_address = shipping_address_form.save(commit=False)
                shipping_address.shipping = shipping
                shipping_address.save()
            else:
                transaction.set_rollback(True)
                return redirect(order.get_checkout_url)


        # Create Guest
        if guest_form.is_valid():
            guest = guest_form.save()
        else:
            transaction.set_rollback(True)
            return redirect(order.get_checkout_url)

        # Update Order
        order.guest = guest
        order.status = "PENDING"
        order.save()

        return redirect(order.get_payment_url)