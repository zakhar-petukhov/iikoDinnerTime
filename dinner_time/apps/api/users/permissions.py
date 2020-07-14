from rest_framework.permissions import BasePermission


class IsCompanyAuthenticated(BasePermission):
    """
    Allows access only to authenticated company or superuser.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_company or request.user.is_superuser)
