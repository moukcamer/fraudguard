# apps/api/authentication.py
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from datetime import datetime, timedelta

User = get_user_model()

class JWTAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return None
        token = auth.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                raise AuthenticationFailed('User inactive')
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')