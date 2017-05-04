from django.conf.urls import include, url

urlpatterns = [
    url(r'^otp/', include('phone_login.urls', namespace='phone_login'),),
]
