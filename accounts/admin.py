from django.contrib import admin
from accounts.models import *

# Register your models here.

# ................***...............Profile................***............


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone']

    class Meta:
        model = UserAccount

admin.site.register(UserAccount, UserAccountAdmin)


# ................***...............CustomerInfo................***............

class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']

    class Meta:
        model = CustomerInfo

admin.site.register(CustomerInfo, CustomerInfoAdmin)


# admin.site.register(CustomerLocation)


# ................***...............CafeStaffInformation................***............


class CafeStaffInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff_id', 'name', 'email', 'is_manager','is_barista', 'is_delivery_boy', 'is_staff']

    class Meta:
        model = CafeStaffInformation

admin.site.register(CafeStaffInformation, CafeStaffInformationAdmin)


# ................***...............StaffFcmDevice................***............


class StaffFcmDeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'cafe_staff', 'device_id']

    class Meta:
        model = StaffFcmDevice

admin.site.register(StaffFcmDevice, StaffFcmDeviceAdmin)


# ................***...............StaffFcmDevice................***............


class CustomerFcmDeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'device_id']

    class Meta:
        model = CustomerFcmDevice

admin.site.register(CustomerFcmDevice, CustomerFcmDeviceAdmin)