# myapp/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

class ReadOnlyOrAuthenticatedCreate(permissions.BasePermission):
    """
    Allows read-only access to anyone, but only authenticated users can create.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True 
        else:
            return request.user and request.user.is_authenticated
