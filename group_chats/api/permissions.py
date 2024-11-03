from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacherforFile(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Teacher'