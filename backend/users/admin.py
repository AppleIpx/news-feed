from django.contrib import admin
from django.contrib.admin import register

from .models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "email",
        "username",
        'password',
        "first_name",
        "last_name",
        "is_staff",
    )
    list_display = (
        "pk",
        'email',
        "username",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_filter = (
        'first_name',
        'last_name',
    )

    ordering = ["email", "first_name", "last_name", ]
