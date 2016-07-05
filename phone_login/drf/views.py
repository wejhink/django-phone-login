import json

from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate, logout

from phone_login.models import PhoneToken


@api_view(['POST'])
@authentication_classes([])
def create_otp(request):
    data = json.loads(request.body)
    phone_number = data.get("phone_number")
    if phone_number:
        token = PhoneToken.create_otp_for_number(phone_number)
        if token:
            return Response({"status": "success"})
        else:
            return Response({"status": "failure", "message": "Reached max limit for the day."})
    else:
        return Response({"statue": "failure"})


@api_view(['POST'])
@authentication_classes([])
def check_otp(request):
    data = json.loads(request.body)
    otp = data.get("otp")
    phone_number = data.get("phone_number")
    user = authenticate(otp=otp, phone_number=phone_number)
    if user:
        last_login = user.last_login
        login(request, user)
        return Response({"user_id": user.pk, "last_login": last_login, "status": "success", "token": user.auth_token.key})
    else:
        return Response({"status": "failure", "message": "invalid otp"})


@api_view(['GET'])
def user_details(request):
    user = request.user
    if user.is_authenticated():
        return Response({"user_id": user.pk, "last_login": user.last_login, "token": user.auth_token.key})
    return Response({"status": "failure", "message": "User not logged in."})
