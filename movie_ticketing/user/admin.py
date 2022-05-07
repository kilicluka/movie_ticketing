from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


@admin.register(UserProfile)
class UserAdmin(UserAdmin):
    list_display = ["email", "is_staff", "is_superuser", "created_at", "updated_at"]
    search_fields = ["email"]
    list_filter = ["is_staff", "is_superuser"]
    ordering = ["-updated_at"]

    fieldsets = ((None, {"fields": ("email", "password")}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
