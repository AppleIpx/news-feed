from django.contrib import admin
from . import models


@admin.register(models.BlogPost)
class BlockPostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'image',
        'created_at',
    )
    list_filter = (
        'title',
        'created_at',
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'blog_post',
        'user',
        'text',
        'created_at',
    )
    list_filter = (
        'blog_post',
        'user',
        'created_at',
    )
