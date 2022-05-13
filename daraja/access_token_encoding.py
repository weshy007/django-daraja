import base64
from django.conf import settings

def generate_password(dates):
    # data_to_encode = settings.CONSUMER_KEY+settings.SECRET_KEY+dates
    data_to_encode = settings.BUSINESS_SHORT_CODE+settings.LIPA_NA_MPESA_PASSKEY+dates 

    encoded_string = base64.b64encode(data_to_encode.encode())
    decoded_passkey = encoded_string.decode('utf-8')
    
    return decoded_passkey