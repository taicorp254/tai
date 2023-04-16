from django.contrib import admin
from .models import Page_users
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(Page_users, UserAdmin)