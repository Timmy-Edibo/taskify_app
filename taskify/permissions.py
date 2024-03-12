# bus_ticketing/permissions.py
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to anyone
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        # Check if the user is in the 'admin' group
        return request.user and request.user.groups.filter(name="admin").exists()


class IsStaffUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to anyone
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        # Check if the user is in the 'admin' group
        return request.user and request.user.role.name.lower() in [
            "admin",
            "manager",
            "staff",
        ]


def check_permission(user):
    if user.role:
        if (
            user
            and user.is_authenticated
            and user.is_staff
            and user.role.name.lower() == "admin"
        ):
            return "is_admin"
        if (
            user
            and user.is_authenticated
            and user.is_staff
            and user.role.name.lower() == "staff"
        ):
            return "is_staff"
        if (
            user
            and user.is_authenticated
            and not user.is_staff
            and user.role.name.lower() == "passenger"
        ):
            return "is_passenger"

        if (
            user
            and user.is_authenticated
            and not user.is_staff
            and user.role.name.lower() == "manager"
        ):
            return "is_manager"
    else:
        print("no role attached", user.role)
        return "error"
