from django.urls import include, path
from . import views
app_name = "payments"

urlpatterns = [
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.handle_payment_success, name='handle_payment_success'),
    path('payment-failure/', views.handle_payment_failure, name='handle_payment_failure'),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
]