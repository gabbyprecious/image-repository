from django.contrib.auth import get_user_model
from rest_framework import exceptions
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
import six
from jose import JWTError, jwt


User = get_user_model()

ENCRYPTION_ALGORITHM = "HS256"




def generate_auth_token(user):
    """
    Generate a user auth token
    :param user
    :return:
    """
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token)}


def decrypt_token(token):
    """
    Returns decrypted token if valid, or returns None otherwise
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ENCRYPTION_ALGORITHM])
        return payload

    except JWTError:
        # eg: jose.exceptions.ExpiredSignatureError: Signature has expired.
        return None



class CookieJWTAuthentication(BaseAuthentication):
    """
    Custom Authentication Class that authenticates users from cookies (http-only)
    instead of from Authorization key in headers
    """

    def authenticate(self, request):
        """
        Is required to be implemented (from BaseAuthentication)
        :param request:
        :return:
        """
        authorization_cookie = request.COOKIES.get("Authorization") or request.headers.get("Authorization")

        if not authorization_cookie:
            return None
        try:
            access_token = authorization_cookie.split(" ")[1]
            payload = decrypt_token(access_token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("access_token expired")
        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing")

        if not payload:
            raise exceptions.AuthenticationFailed("Token expired")

        user = User.objects.filter(id=payload["user_id"]).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive")

        self.enforce_csrf(request)
        return user, None

    def enforce_csrf(self, request):
        """
        Enforces CSRF Validation
        :param request:
        :return:
        """
        return
