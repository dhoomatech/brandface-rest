from django.contrib import admin
from django.utils.html import format_html
from .models import *

class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1
    fields = ['platform', 'url']
    show_change_link = True


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    fields = ['title', 'description']
    show_change_link = True


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['image', 'caption']
    show_change_link = True


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'owner', 'unique_name', 'phone', 'email', 'created_at')
    search_fields = ('business_name', 'unique_name', 'owner__username', 'email')
    list_filter = ('created_at',)
    prepopulated_fields = {'unique_name': ('business_name',)}
    inlines = [SocialMediaInline, ServiceInline, GalleryImageInline, PhoneNumberInline]


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('platform', 'profile', 'url')
    search_fields = ('platform__name', 'profile__business_name')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile','icon_or_image')
    search_fields = ('title', 'profile__business_name')
    def icon_or_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:30px;" />', obj.image.url)
        elif obj.icon:
            return format_html('<i class="{}"></i>', obj.icon)
        return "-"
    icon_or_image.short_description = "Preview"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'caption')
    search_fields = ('caption', 'profile__business_name')


@admin.register(SocialMediaPlatform)
class SocialMediaPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


class SocialMediaPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_preview')

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="height:25px;" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "Icon"