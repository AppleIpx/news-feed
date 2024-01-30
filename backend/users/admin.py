from django.contrib import admin
from .models import User

from django.contrib.admin import register


@register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "email",
        "username",
        'password',
        "first_name",
        "last_name",
    )
    list_display = (
        "pk",
        'email',
        "username",
        "first_name",
        "last_name",
    )
    list_filter = (
        'first_name',
        'last_name',
    )

    ordering = ["email", "first_name", "last_name", ]
