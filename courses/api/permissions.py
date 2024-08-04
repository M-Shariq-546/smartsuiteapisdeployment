from rest_framework.permissions import BasePermission
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'Super Admin':
            return True
        return False