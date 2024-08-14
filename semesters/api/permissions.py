from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated and request.user.role == 'Student':
            return True
            
        
        if request.user.is_authenticated and request.user.role == 'Super Admin':
            return True
        return False