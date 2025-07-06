from django.contrib import admin
from .models import *

@admin.register(InstagramConfig)
class InstagramConfigAdmin(admin.ModelAdmin):
    list_display = ('profile', 'instagram_user_id', 'updated_at')
    search_fields = ('profile__business_name', 'instagram_user_id')
    autocomplete_fields = ['profile']


@admin.register(SocialMediaConfig)
class SocialMediaConfigAdmin(admin.ModelAdmin):
    list_display = ('profile', 'google_api_key')
    search_fields = ('profile__business_name',)
    autocomplete_fields = ['profile']
    list_select_related = ['profile']


@admin.register(GoogleReview)
class GoogleReviewAdmin(admin.ModelAdmin):
    list_display = ('profile', 'author_name', 'rating', 'time')
    search_fields = ('author_name', 'profile__business_name')
    list_filter = ('rating', 'time')
    readonly_fields = ('time',)
    autocomplete_fields = ['profile']
    list_select_related = ['profile']