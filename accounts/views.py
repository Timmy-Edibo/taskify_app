from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied

from rest_framework.permissions import IsAdminUser, IsAuthenticated

from taskify.permissions import check_permission
from .models import CustomUser
from .serializers import *

from rest_framework.exceptions import APIException
from .permissions import CreateUserPermission
from .helpers import *
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import CustomRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _


class CustomUserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [CreateUserPermission]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        permission = check_permission(user)

        if permission == "is_admin":
            return CustomUser.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        result = check_permission(user)
        queryset = super().get_queryset()

        if result == "error":
            raise ValidationError({"detail": "Specify role for user to access data"})
        elif result == "admin":
            return queryset

        # Perform permission checks for DELETE request
        if self.request.method == "DELETE":
            user = self.get_object()
            if user.role.name != "admin":
                raise PermissionDenied("Only admin can delete Users/Team members")

        return queryset

    def perform_destroy(self, instance):
        instance.delete()

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return CustomUserUpdateSerializer
        return super().get_serializer_class()


"""
Admin Endpoints
"""


class DisableUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if check_permission(user):
            user = CustomUser.objects.get(pk=kwargs["pk"])
            user.is_active = False
            user.save()

            serializer = CustomUserResponseSerializer(user)
            data = {"detail": "User Enabled successfully", "user": serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )


class EnableUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if check_permission(user):
            user = CustomUser.objects.get(pk=kwargs["pk"])
            user.is_active = True
            user.save()

            serializer = CustomUserResponseSerializer(user)
            data = {"detail": "User Enabled successfully", "user": serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )


class GetCurrentUser(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    @staticmethod
    def get(request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


"""
    Role Endpoints
"""


class RoleAPIView(generics.ListCreateAPIView):
    queryset = Role.objects.all().order_by("id")
    serializer_class = RoleSerializer

    def get_queryset(self):
        return super().get_queryset()

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserByEmail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    @staticmethod
    def get(request, email):
        passenger = CustomUser.objects.filter(email=email).first()
        serializer = UserSerializer(passenger)
        return Response(serializer.data)


class CustomRegisterView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer
    permission_classes = []

    def generate_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return {"access": str(access_token), "refresh": str(refresh)}

    def post(self, request, *args, **kwargs):
        try:
            role_name = request.data.get("role")
            role = get_object_or_404(Role, name__icontains=role_name)

            username, error = create_username(request)
            if not username:
                raise APIException(detail=error[0], code=400)

            user = CustomUser.objects.create(
                username=username,
                email=request.data.get("email"),
                password=make_password(request.data.get("password")),
                role=role,
            )

            serializer = UserSerializer(user)
            tokens = self.generate_tokens(user)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"user": serializer.data, "tokens": tokens},
                status=status.HTTP_201_CREATED,
            )
        except Role.DoesNotExist:
            raise ValidationError({"error": f"Role with name '{role_name}' not found."})

        except CustomUser.DoesNotExist:
            raise ValidationError({"error": "Error creating user."})

        except Exception as e:
            print(e)
            if "unique constraint" in str(e).lower() and "username" in str(e).lower():
                raise ValidationError({"error": "User with email exist"})

            elif "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise ValidationError({"error": "User with email exist"})

            raise ValidationError({"error": "An unexpected error occurred."})


class CustomPasswordResetView(PasswordResetConfirmView):
    def post(self, request, *args, **kwargs):
        """
        This method is called when the form is valid and the reset email is sent.
        You can override it to customize email content and data passed to the template.
        """
        email = request.data.get("email", None)
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise ValidationError("User not found")

        # Generate the reset token
        current_site = get_current_site(request)
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Get the current site domain and protocol
        protocol = "https" if self.request.is_secure() else "http"
        domain = current_site.domain if self.request.is_secure() else "localhost:3000"

        # Create the reset link URL
        reset_url = reverse(
            "password_reset_confirm",
            kwargs={
                "uidb64": uidb64,
                "token": token,
            },
        )

        reset_url = f"{protocol}://{domain}{reset_url}"

        # Render your custom email template with the data
        email_template = render_to_string(
            "accounts/password_reset_email.html",
            {
                "email": email,
                "user": user.username,
                "protocol": protocol,
                "domain": domain,
                "reset_url": reset_url,
                "uidb64": uidb64,
                "token": token,
                "site_name": "Ammani Transport & Logistics Ticketting App",
            },
        )

        # Send the custom email
        subject = "Password Reset Request"
        message = "You have requested a password reset for your account."
        from_email = "Ammani Transport and Logistics Ticketing App"
        recipient_list = [email]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,
            html_message=email_template,
        )

        return Response(
            data={"detail": "Password reset link has been sent to your email."},
            status=status.HTTP_200_OK,
        )


class CustomPasswordResetConfirmView(APIView):
    serializer_class = CustomUserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password1 = request.data.get("new_password1", None)
        new_password2 = request.data.get("new_password2", None)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(id=uid)
        except (TypeError, ValueError, UnicodeDecodeError):
            raise ValidationError({"error": ["Invalid value"]})

        if not default_token_generator.check_token(user, token):
            raise ValidationError({"error": ["Invalid value"]})

        if new_password1 != new_password2:
            raise ValidationError({"error": ["Passwords do not match"]})

        form = SetPasswordForm(
            user, {"new_password1": new_password1, "new_password2": new_password2}
        )
        if form.is_valid():
            form.save()
        else:
            raise ValidationError({"error": form.errors})

        return Response(
            {"detail": _("Password has been reset with the new password.")},
            status=status.HTTP_200_OK,
        )
