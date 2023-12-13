import moncashify
from typing import Any
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView

from apps.catalog.models import Product
from apps.sales.models import Payment


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()[:6]
        return context
    
    
class AboutPageView(TemplateView):
    template_name = 'main/about.html'


def handle_moncash_payment_notification(request):
    transaction_id = request.GET.get('transactionId')

    moncash = moncashify.API(
        client_id=settings.MONCASH_CLIENT_ID,
        secret_key=settings.MONCASH_CLIENT_SECRET,
        debug=settings.MONCASH_DEBUG
    )

    transaction = moncash.transaction_details_by_transaction_id(transaction_id)
    details = transaction['payment']

    try:
        payment: Payment = Payment.objects.get(reference=details['reference'])
        payment.details = details

        if details['message'] == 'successful':
            payment.status = 'COMPLETED'
            payment.save()
        else:
            payment.status = 'FAILED'
            payment.save()
        

        return JsonResponse({ "status": "ok" })
    except Payment.DoesNotExist:
        return JsonResponse({ "status": "error" }, status=404)
    

def handle_moncash_payment_alert(request):
    transaction_id = request.GET.get('transactionId')

    moncash = moncashify.API(
        client_id=settings.MONCASH_CLIENT_ID,
        secret_key=settings.MONCASH_CLIENT_SECRET,
        debug=settings.MONCASH_DEBUG
    )

    transaction = moncash.transaction_details_by_transaction_id(transaction_id)
    details = transaction['payment']

    if details['message'] == 'successful':
        context = {
            'success': True,
            'message': 'Payment completed successfully'
        }
    else:
        context = {
            'success': False,
            'message': 'Payment failed'
        }
    
    return render(request, 'sales/payment_alert.html', context=context)

    