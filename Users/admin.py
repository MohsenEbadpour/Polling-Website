from django.contrib import admin

# Register your models here.
from .models import User,Notification

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User

class NotificationAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        
admin.site.register(User,UserAdmin)
admin.site.register(Notification,NotificationAdmin)