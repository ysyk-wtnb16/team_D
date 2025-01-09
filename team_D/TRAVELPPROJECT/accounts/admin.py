from django.contrib import admin

from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

    list_display_links = ('id', 'username')

admin.site.register(CustomUser, CustomUserAdmin)