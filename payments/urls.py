# payments/urls.py
from django.urls import path
from . import views

app_name = 'payments' # For namespacing your URLs

urlpatterns = [
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.handle_payment_success, name='payment_success'),
]