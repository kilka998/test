
from company.models import UserToken, Employee
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication

from rest_framework.authentication import TokenAuthentication


class UserTokenAuthentication(TokenAuthentication):

    model = UserToken

    def authenticate_credentials(self, key):
        _, token = super().authenticate_credentials(key)
        user = Employee.objects.get(id=token.user_id)
        return user, token


class ApiCsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        if request.get_full_path().startswith('/api'):
            return
        return super().enforce_csrf(request)