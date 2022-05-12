from rest_framework import serializers
 

class MakePaymentSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    amount = serializers.CharField()