from rest_framework.permissions import BasePermission


class CreateUserPermission(BasePermission):
    def has_permission(self, request, view):
        # Allow admin user to list users
        if request.method == "GET":
            return (
                request.user and request.user.is_authenticated and request.user.is_staff
            )

        elif request.method == "POST":
            return True

        return False


class AdminCreateUserPermission(BasePermission):
    def has_permission(self, request, view):
        # Allow admin user to list users
        if request.method in ["GET", "POST"]:
            return (
                request.user and request.user.is_authenticated and request.user.is_staff
            )

        return False
