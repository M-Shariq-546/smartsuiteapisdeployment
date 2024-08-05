from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Super Admin'

class IsTeacherforFile(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Teacher'


class IsStudentForFiles(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated and request.user.role == 'Student'
        return False
class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated and request.user.role == 'Teacher'
        return False

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return False
