# views.py

from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.utils.crypto import get_random_string
import hashlib
from django.conf import settings
from rest_framework.response import Response
from  rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from home.models import *
from home.serializer import paymentserializer

def generate_hash(hash_str):

    return hashlib.sha512(hash_str.encode('utf-8')).hexdigest()

def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            return HttpResponse("Amount is required", status=400)

        txnid = get_random_string(length=10)  # Generate a unique transaction ID
        email = 'customer@example.com'  # Replace with actual customer email

        # PayU parameters
        data = {
            'key': settings.PAYU_MERCHANT_KEY,
            'txnid': txnid,
            'amount': str(amount),  # Convert amount to string
            'productinfo': 'Test Product',
            'firstname': 'John',
            'email': email,
            'phone': '1234567890',
            'surl': request.build_absolute_uri('/payment/success/'),
            'furl': request.build_absolute_uri('/payment/failure/'),
            'payu_url': settings.PAYU_TEST_URL
        }

        # Concatenate parameters with '|', and append the salt at the end
        hash_str = '|'.join([
            data['key'],
            data['txnid'],
            data['amount'],
            data['productinfo'],
            data['firstname'],
            data['email'],
            '',  # udf1
            '',  # udf2
            '',  # udf3
            '',  # udf4
            '',  # udf5
            '',  # udf6 (if used)
            '',  # udf7 (if used)
            '',  # udf8 (if used)
            '',  # udf9 (if used)
            '',  # udf10 (if used)
        ]) + '|' + settings.PAYU_MERCHANT_SALT

        # Generate hash
        data['hash'] = generate_hash(hash_str)

        # Render the redirect form to PayU
        return render(request, 'redirect_to_payu.html', {'data': data})

    return render(request, 'initiate_payment.html')






class payment_success(APIView):
    @method_decorator(csrf_exempt)
    def post(self,request):
        serializer=paymentserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'payment successfully'})
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
def payment_failure(request):
    return HttpResponse('Payment failed', status=400)


