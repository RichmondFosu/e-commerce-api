from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Allows only the owner of a product to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in SAFE_METHODS:
            return True

        # Write permissions only for the owner
        return obj.created_by == request.user
