from phonenumber_field.formfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PhoneToken

class PhoneTokenCreateSerializer(ModelSerializer):
    phone_number = serializers.CharField(validators=PhoneNumberField().validators)

    class Meta:
        model = PhoneToken
        fields = ('pk','phone_number',)

class PhoneTokenValidateSerializer(ModelSerializer):
    pk = serializers.IntegerField()
    otp = serializers.CharField(max_length=40)

    class Meta:
        model = PhoneToken
        fields = ('pk','otp')
