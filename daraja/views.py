import json

import requests
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .access_token_encoding import generate_password
from .date_formatting import formatted_date
from .generate_token import generate_token
from .serializer import MakePaymentSerializer


# Create your views here.
class InitiateSTKPush(GenericAPIView):
    serializer_class = MakePaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)

        request_data = request.data
        amount = request_data.get("amount")
        phone_number = request_data.get("phone_number")

        payment_response = self.initiate_mpesa_stk(amount=amount, phone_number=phone_number)

        return Response(payment_response)

    def initiate_mpesa_stk(self, amount:str, phone_number:str) -> dict:
        access_token = generate_token()
        formatted_time = formatted_date()
        password = generate_password(formatted_time)

        headers = {
            'Authorization': 'Bearer %s' % access_token
        }

        payload = {
            "BusinessShortCode":"174379",    
            "Password": password,    
            "Timestamp": formatted_time,    
            "TransactionType": "CustomerPayBillOnline",    
            "Amount": amount,    
            "PartyA": phone_number,    
            "PartyB":"174379",    
            "PhoneNumber": phone_number,    
            "CallBackURL":"https://mydomain.com/pat",    
            "AccountReference":"ONLINE PAYMENT",    
            "TransactionDesc":"Test"
        }

        response = requests.post(
            settings.API_RESOURCE_URL, headers=headers, json=payload)

        string_response = response.text
        string_object = json.loads(string_response)

        if 'errorCode' in string_object:
            print('ERROR', string_object)
            # PASSED REQUEST
            return string_object
        else:
            merchant_request_id = string_object["MerchantRequestID"]
            checkout_request_id = string_object["CheckoutRequestID"]
            response_code = string_object["ResponseCode"]
            response_description = string_object["ResponseDescription"]
            customer_message = string_object["CustomerMessage"]

            data = {
                "MerchantRequestID": merchant_request_id,
                "CheckoutRequestID": checkout_request_id,
                "ResponseCode": response_code,
                "ResponseDescription": response_description,
                "CustomerMessage": customer_message,
            }

            return data
