from twilio.rest import TwilioRestClient
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

NOT_CONFIGURED_MESSAGE = """Cannot initialize Twilio message client.
Required settings variables TWILIO_ACCOUNT_SID, or
TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing"""

def load_rest_client():
    twilio_account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID')
    twilio_auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN')

    if not all([twilio_account_sid, twilio_auth_token]):
        raise ImproperlyConfigured(NOT_CONFIGURED_MESSAGE)

    return TwilioRestClient(twilio_account_sid,
                                          twilio_auth_token)


class MessageClient(object):
    def __init__(self):
        self.twilio_number = getattr(settings, 'TWILIO_NUMBER')
        if self.twilio_number:
            self.twilio_client = load_rest_client()

    def send_message(self, body, to):
        try:
            return self.twilio_client.messages.create(
              body=body,
              to=to,
              from_=self.twilio_number
            )
        except AttributeError:
            print body
