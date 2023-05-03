from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from .models import *
class AwarenessAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(Data)
admin.site.register(UserContact)
admin.site.register(Awareness, AwarenessAdmin)
admin.site.register(Message)

