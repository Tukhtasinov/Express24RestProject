from rest_framework.permissions import BasePermission
from .models import UserRole


class IsAdminPermission(BasePermission):

    def has_permission(self, request, view):
        try:
            admin_role = UserRole.objects.get(user=request.user).role.name.lower()
        except UserRole.DoesNotExist:
            return False
        return admin_role == 'admin'


class IsAdminOrDeliverPermission(BasePermission):

    def has_permission(self, request, view):
        try:
            user_role = UserRole.objects.get(user=request.user).role.id
        except UserRole.DoesNotExist:
            return False
        if user_role == 1 or user_role == 2:
            print('Test successful')
            return True
        else:
            return False

