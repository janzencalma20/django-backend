import firebase_admin
from django.contrib.auth.models import User
from django.utils import timezone
from firebase_admin.exceptions import FirebaseError
from rest_framework import authentication
import firebase_admin.auth as auth
from firebase_admin import credentials

from Dimensions_api.settings import env
from firebase_authentication.exceptions import NoAuthToken, InvalidAuthToken

cred=credentials.Certificate(
{
  "type": env("FIREBASE_SERVICE_ACCOUNT"),
  "project_id": env("FIREBASE_PROJECTID"),
  "private_key_id": env("FIREBASE_PRIVATEKEYID"),
  "private_key": env.str("FIREBASE_PRIVATEKEY", multiline=True),
  "client_email": env("FIREBASE_CLIENT_EMAIL"),
  "client_id": env("FIREBASE_CLIENTID"),
  "auth_uri": env("FIREBASE_AUTHURL"),
  "token_uri": env("FIREBASE_TOKENURL"),
  "auth_provider_x509_cert_url": env("FIREBASE_AUTHPROVIDER"),
  "client_x509_cert_url": env("FIREBASE_CLIENT_CERT")
}
)

default_app = firebase_admin.initialize_app(cred)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as err:
            raise InvalidAuthToken("Invalid auth token")
            pass

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception as err:
            raise FirebaseError()

        user, created = User.objects.get_or_create(username=uid)
        # user.profile.last_activity = timezone.localtime()

        return (user, None)