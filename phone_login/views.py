import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate

from .models import PhoneToken

# Create your views here.
@csrf_exempt
@require_POST
def create_otp(request):
    data = json.loads(request.body)
    phone_number = data.get("phone_number")
    if phone_number:
        token = PhoneToken.create_otp_for_number(phone_number)
        if token:
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "failure", "message": "Reached max limit for the day."})
    else:
        return JsonResponse({"statue": "failure"})

@csrf_exempt
@require_POST
def check_otp(request):
    data = json.loads(request.body)
    otp = data.get("otp")
    phone_number = data.get("phone_number")
    user = authenticate(otp=otp, phone_number=phone_number)
    if user:
        phone_token = PhoneToken.objects.get(phone_number=phone_number, otp=otp)
        last_login = user.last_login
        login(request, user)
        return JsonResponse({"user_id": user.pk, "last_login": last_login, "status": "success"})
    else:
        return JsonResponse({"status": "failure", "message": "invalid otp"})
