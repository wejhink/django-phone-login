from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser, PhoneToken


class PhoneTokenAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'timestamp', 'attempts', 'used')
    search_fields = ('phone_number', )
    list_filter = ('timestamp', 'attempts', 'used')
    readonly_fields = ('phone_number', 'otp', 'timestamp', 'attempts')


class PhoneUserAdmin(UserAdmin):
    search_fields = ('username', 'phone_number', 'first_name',
                     'last_name', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'phone_number')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(CustomUser, PhoneUserAdmin)
admin.site.register(PhoneToken, PhoneTokenAdmin)
