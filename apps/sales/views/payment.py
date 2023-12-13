from typing import Any
import moncashify
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView

from apps.sales.models import Order
from apps.sales.models import PaymentMethod, Payment


class PaymentView(DetailView):
    template_name = 'sales/payment.html'
    queryset = Order.objects.with_items()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['payment_methods'] = PaymentMethod.objects.filter(available=True)
        return context


def process_payment(request: HttpRequest, pk: int, reference: str, alias: str):
    order = get_object_or_404(Order, pk=pk, reference=reference)
    method = get_object_or_404(PaymentMethod, alias=alias)

    if order.status != 'PENDING':
        return redirect(order.get_payment_url)

    if hasattr(order, 'payment'):
        return redirect(order.get_payment_url)
    
    # Create Payment
    payment: Payment = Payment.objects.create(
        order=order,
        method=method,
        amount=order.total,
    )

    if method.alias == 'MONCASH':
        moncash = moncashify.API(
            client_id=settings.MONCASH_CLIENT_ID,
            secret_key=settings.MONCASH_CLIENT_SECRET,
            debug=settings.MONCASH_DEBUG
        )

        payment = moncash.payment(
            order_id=payment.reference,
            amount=payment.amount,
        )
    else:
        NotImplementedError(f'Payment method {method.name} is not implemented')
    
    return redirect(payment.get_redirect_url())
