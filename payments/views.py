from django.shortcuts import render, get_object_or_404

# Create your views here.
# payments/views.py
import razorpay
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
import json

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Assume Event model is imported from your events app
# from events.models import Event

def initiate_payment(request, event_id):
    if request.method == "GET":
        # event = get_object_or_404(Event, id=event_id)
        amount_inr = 200  # Fixed entry pass for all events
        amount = amount_inr * 100  # Convert to paisa
        currency = 'INR'

        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": currency,
            "payment_capture": '0'
        })

        context = {
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': amount,
            'currency': currency,
            'order_id': razorpay_order['id'],
            # 'name': event.name,
            # 'description': event.description,
            # 'event_id': event.id
        }
        return render(request, 'payments/payment_page.html', context)
    return HttpResponseBadRequest("Method not allowed")

@csrf_exempt
def handle_payment_success(request):
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result is not None:
                # If verification is successful, capture the payment
                amount = 50000 # This should be the same amount as when the order was created
                razorpay_client.payment.capture(payment_id, amount)

                # Update your order status in the database
                # For example:
                # order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                # order.payment_id = payment_id
                # order.signature = signature
                # order.status = 'success'
                # order.save()

                return render(request, 'payments/payment_success.html')
            else:
                return render(request, 'payments/payment_failure.html', {'error': 'Signature verification failed'})
        except Exception as e:
            return render(request, 'payments/payment_failure.html', {'error': str(e)})
    return HttpResponseBadRequest("Method not allowed")

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handle_payment_failure(request):
    return render(request, 'payments/payment_failure.html', {'error': 'Payment failed or cancelled.'})