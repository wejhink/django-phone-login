from django.conf.urls import url, include

from .views import create_otp, check_otp

urlpatterns = [
    url(r'^create_otp/$', create_otp, name="create_otp"),
    url(r'^check_otp/$', check_otp, name="check_otp"),
]
