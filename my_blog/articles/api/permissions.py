from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsWriterOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `writer` attribute.
    """

    def has_object_permission(self, request, view, obj):
        _ = view

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.writer == request.user


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        _ = view

        if request.method in SAFE_METHODS:
            return True
        return False
