from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, object):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_staff
        )


class AuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, object):
        return (
            request.method in permissions.SAFE_METHODS
            or object.author == request.user
        )
