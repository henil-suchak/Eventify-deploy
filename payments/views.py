from django.shortcuts import render

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

def initiate_payment(request):
    if request.method == "GET":
        # Example: You might get amount from a product in your database
        amount = 50000  # Amount in paisa (e.g., 500 INR = 50000 paisa)
        currency = 'INR'

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                            currency=currency,
                                                            payment_capture='0')) # '0' means manual capture, '1' for auto capture

        # Store order details in your database if needed (e.g., Order model)
        # order = Order.objects.create(
        #     amount=amount / 100,  # Convert back to INR for your database
        #     razorpay_order_id=razorpay_order['id'],
        #     status='created'
        # )
        # order.save()

        context = {
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': amount,
            'currency': currency,
            'order_id': razorpay_order['id'],
            'name': 'Your Company Name',
            'description': 'Product/Service Description',
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