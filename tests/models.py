from phone_login.models import PhoneNumberAbstactUser


class CustomUser(PhoneNumberAbstactUser):
    REQUIRED_FIELDS = ['phone_number', 'email']

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username
