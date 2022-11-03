from django.contrib import admin
from dashboard.models import *

# Register your models here.

# ................***...............Slider................***............


class SliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']

    class Meta:
        model = Slider

admin.site.register(Slider, SliderAdmin)


# ................***...............AboutUs................***............


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

    class Meta:
        model = AboutUs

admin.site.register(AboutUs, AboutUsAdmin)


# ................***...............Gallery................***............


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']

    class Meta:
        model = Gallery

admin.site.register(Gallery, GalleryAdmin)


# ................***...............OwnerInformation................***............


class OwnerInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']

    class Meta:
        model = OwnerInformation

admin.site.register(OwnerInformation, OwnerInformationAdmin)


# ................***...............Blog................***............


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']

    class Meta:
        model = Blog

admin.site.register(Blog, BlogAdmin)


# ................***...............ArabikaWork................***............


class ArabikaWorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']

    class Meta:
        model = ArabikaWork

admin.site.register(ArabikaWork, ArabikaWorkAdmin)


# ................***...............ArabikaHistory................***............


class ArabikaHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','serial_no', 'created_at']

    class Meta:
        model = ArabikaHistory

admin.site.register(ArabikaHistory, ArabikaHistoryAdmin)


