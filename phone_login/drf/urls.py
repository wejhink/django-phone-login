from django.conf.urls import url

from .views import create_otp, check_otp, user_details, logout

urlpatterns = [
    url(r'^create_otp/$', create_otp, name="api_create_otp"),
    url(r'^check_otp/$', check_otp, name="api_check_otp"),
    url(r'^user_details/$', user_details, name="api_user_details"),
]
