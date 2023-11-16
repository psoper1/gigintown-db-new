from django.contrib import admin
from .models import *
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass