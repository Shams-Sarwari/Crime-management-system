from django.contrib import admin
from .models import User, StaffProfile, Address, WorkPlace, DriverProfile
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'licence_num', 'is_staff', 'is_driver', ]

@admin.register(StaffProfile)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']

@admin.register(DriverProfile)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'licence_num']


admin.site.register(Address)
admin.site.register(WorkPlace)