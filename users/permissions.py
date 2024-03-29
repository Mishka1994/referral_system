from rest_framework.permissions import BasePermission

from users.models import User


class IsAuthorization(BasePermission):

    def has_permission(self, request, view):
        input_phone = request.data.get('phone')
        if input_phone is None:
            input_phone = request.query_params.get('phone')
            if input_phone is None:
                return False
        user = User.objects.filter(phone=input_phone).first()
        if user is None:
            return False
        else:
            return user.is_active
