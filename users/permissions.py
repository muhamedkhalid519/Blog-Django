from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        if hasattr(obj, 'author'):
            return obj.author == request.user

        return obj == request.user