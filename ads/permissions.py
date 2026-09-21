from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    - SAFE_METHODS (GET, HEAD, OPTIONS) — всем.
    - POST — авторизованным.
    - PUT/PATCH/DELETE — автору объекта или админу.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role == 'admin':
            return True
        return obj.author == request.user
