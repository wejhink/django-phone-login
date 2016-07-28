import json

from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate, logout

from phone_login.models import PhoneToken

from phone_login.utils import (failure, success,
        unauthorized, too_many_requests, user_detail)

@api_view(['POST'])
@authentication_classes([])
def create_otp(request):
    data = json.loads(request.body)
    phone_number = data.get("phone_number")
    if phone_number:
        token = PhoneToken.create_otp_for_number(phone_number)
        if token:
            response, status = success()
            return Response(response, status = status)
        else:
            response, status = too_many_requests()
            return Response(response, status = status)
    else:
        response, status = failure("Phone number is not given")
        return Response(response, status = status)

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
        response, status = user_detail(user, last_login)
        return Response(response, status = status)
    else:
        response, status = failure("Invalid OTP")
        return Response(response, status = status)


@api_view(['GET'])
def user_details(request):
    user = request.user
    if user.is_authenticated():
        response, status = user_detail(user, user.last_login)
        return Response(response, status = status)
    response, status = unauthorized()
    return Response(response, status = status)
