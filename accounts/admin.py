from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom Admin configuration for the User model.
    Extends Django's BaseUserAdmin for consistent user management
    while allowing custom fields like name, phone, and user_type.
    """
    list_display = ("email", "name", "phone", "is_staff", "is_active")
    # list_display = ("email", "name", "phone", "user_type", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "name", "phone")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "phone")}),
        # (_("Personal info"), {"fields": ("name", "phone", "user_type")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

   
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "phone","password","is_active", "is_staff", "is_superuser"),
            # "fields": ("email", "name", "phone","password", "user_type", "is_active", "is_staff", "is_superuser"),
        }),
    )


