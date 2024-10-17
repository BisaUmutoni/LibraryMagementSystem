from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `user`.
        return obj.user == request.user or request.user.is_staff

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'member'
    
class PermitCheckoutBooks(permissions.BasePermission):
   # Custom permission to only allow active users to checkout books.
    def has_permission(self, request, view):
        # Only active users can checkout books
        return request.user and request.user.is_active
    
class IsAdminOrUser(permissions.BasePermission):
   # permission to only allow admin users to edit objects.
   # Read-only permissions are allowed for any request.

    def has_permission(self, request, view):
        return request.user and request.user.is_staff