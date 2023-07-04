from django.contrib import admin
from .models import User, Board, Post
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class UserAdmin(DefaultUserAdmin):
    pass


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Board)
admin.site.register(Post)
