from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Allows anyone to edit or delete products (for demo purposes).
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in SAFE_METHODS:
            return True

        # Write permissions for anyone (demo)
        return True
