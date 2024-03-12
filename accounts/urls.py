# accounts/urls.py
from django.urls import path
from .views import *

# Not Found: /api/v1/administrator/users/14/update/
# administrator
# administrator
urlpatterns = [
    path("users/", CustomUserListView.as_view(), name="customuser-list"),
    path("users/<int:pk>/", CustomUserDetailView.as_view(), name="customuser-detail"),
    path("users/auth/me/", GetCurrentUser.as_view(), name="current-user"),
    path(
        "admin/users/disable/<int:pk>/", DisableUserView.as_view(), name="disable-user"
    ),
    path("admin/users/enable/<int:pk>/", EnableUserView.as_view(), name="enable-user"),
    path("roles/", RoleAPIView.as_view(), name="role-list"),
    path(
        "users/find-user-by-email/<str:email>/",
        GetUserByEmail.as_view(),
        name="user-by-email",
    ),
    path(
        "api/auth/registration/", CustomRegisterView.as_view(), name="custom-register"
    ),
    path(
        "api/auth/password/reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "api/auth/confirm_password_reset/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset",
    ),
    path(
        "api/auth/reset/<str:uidb64>/<str:token>/",
        CustomPasswordResetView.as_view(),
        name="password_reset_confirm",
    ),
]
