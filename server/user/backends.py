import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_prefix = 'token'

    def authenticate(self, request):
        request.user = None
        auth_headers = authentication.get_authorization_header(request).decode("utf-8")
        if not auth_headers:
            return None
        try:
            auth_prefix, auth_token = auth_headers.split(':')
        except ValueError:
            return None
        if not auth_token:
            return None

        if auth_prefix.lower() != self.authentication_prefix:
            return None
        return self._authenticate_credentials(request, auth_token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
