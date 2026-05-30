from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission.

    Read requests are allowed for everyone.
    Write requests are allowed only for object owners or staff users.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        if hasattr(obj, "author"):
            return obj.author == request.user

        if hasattr(obj, "email"):
            return obj.email == request.user.email

        return False
