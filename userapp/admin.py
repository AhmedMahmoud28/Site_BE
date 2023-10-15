from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from userapp import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "username",
    ]

    fieldsets = (
        (
            None,
            {"fields": ("username", "password", "phone")},
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "address",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
