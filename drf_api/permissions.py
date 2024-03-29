from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """custom permission to allow db entries to be viewed publicly
    but can only be updated by the owner"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user