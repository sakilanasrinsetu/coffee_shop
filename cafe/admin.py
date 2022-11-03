from django.contrib import admin
from cafe.models import *

# Register your models here.

# ................***...............CloudCafeInformationAdmin................***............


class CloudCafeInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']

    class Meta:
        model = CloudCafeInformation


admin.site.register(CloudCafeInformation, CloudCafeInformationAdmin)


# ................***...............Cafe................***............


class CafeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']

    class Meta:
        model = Cafe


admin.site.register(Cafe, CafeAdmin)


# ................***...............Notification................***............


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

    class Meta:
        model = Notification


admin.site.register(Notification, NotificationAdmin)


# ................***...............Category................***............


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


# ................***...............Food................***............


class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'sub_title','is_active','is_vat_applicable']

    class Meta:
        model = Food


admin.site.register(Food, FoodAdmin)


# ................***...............FoodOption................***............


class FoodOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','food', 'price']

    class Meta:
        model = FoodOption


admin.site.register(FoodOption, FoodOptionAdmin)


# ................***...............FoodExtra................***............


class FoodExtraAdmin(admin.ModelAdmin):
    list_display = ['id','food', 'title', 'price']

    class Meta:
        model = FoodExtra


admin.site.register(FoodExtra, FoodExtraAdmin)


# ................***...............FoodOrder................***............


class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_no', 'status','customer', 'created_at']

    class Meta:
        model = FoodOrder


admin.site.register(FoodOrder, FoodOrderAdmin)


# ................***...............FoodOrderLog................***............


class FoodOrderLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'order','total_time', 'order_status', 'created_at']

    class Meta:
        model = FoodOrderLog


admin.site.register(FoodOrderLog, FoodOrderLogAdmin)


# ................***...............OrderedItem................***............


class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ['id','food_order', 'quantity', 'food_option', 'status', 'created_at']

    class Meta:
        model = OrderedItem


admin.site.register(OrderedItem, OrderedItemAdmin)


# ................***...............Invoice................***............


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'cafe','order','payment_status', 'created_at']

    class Meta:
        model = Invoice


admin.site.register(Invoice, InvoiceAdmin)


# ................***...............Review................***............


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'rating']

    class Meta:
        model = Review


admin.site.register(Review, ReviewAdmin)




# ................***...............WishList................***............


class WishListAdmin(admin.ModelAdmin):
    list_display = ['id', 'food', 'customer']

    class Meta:
        model = WishList


admin.site.register(WishList, WishListAdmin)


