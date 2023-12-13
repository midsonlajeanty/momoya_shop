"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (
    create_order, 
    CheckoutView, 
    process_checkout,
    PaymentView,
    process_payment
)

app_name = 'sales'

urlpatterns = [
    path('orders/', create_order, name='create_order'),
    path('orders/<int:pk>-<str:reference>/checkout', CheckoutView.as_view(), name='checkout'),
    path('orders/<int:pk>-<str:reference>/process-checkout', process_checkout, name='process_checkout'),
    path('orders/<int:pk>-<str:reference>/payment', PaymentView.as_view(), name='payment'),
    path('orders/<int:pk>-<str:reference>/payment/<str:alias>', process_payment, name='process_payment'),
]
