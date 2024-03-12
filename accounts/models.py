# accounts/models.py
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    phone_number = models.CharField(null=True, blank=True, max_length=15)
    role = models.ForeignKey(
        "Role", blank=True, null=True, on_delete=models.CASCADE, verbose_name="role"
    )
    email = models.EmailField(unique=True, db_index=True)
    address = models.CharField(max_length=255, default="None")
    updated_profile = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("Groups"),
        blank=True,
        related_name="custom_user_groups",  # Provide a unique related_name
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("User Permissions"),
        blank=True,
        related_name="custom_user_permissions",  # Provide a unique related_name
        help_text=_("Specific permissions for this user."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if self.role in ["ADMIN", "DRIVER", "STAFF"]:
            self.is_staff = True
        super(CustomUser, self).save(*args, **kwargs)


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
