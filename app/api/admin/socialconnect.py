from django.contrib import admin
from api.models import SocialConnect

class SocialConnectAdmin(admin.ModelAdmin):
    readonly_fields = ('social_userid', 'social_account_type', 'social_media_count', 'social_username', 
        'user', 'social_access_token', 'social_token_type', 'social_expiry_date',)
    list_display = ('user',)
    list_filter = ('user',)
    fieldsets = (
        ('User details', {'fields': ('social_userid', 'social_account_type', 'social_media_count', 'social_username', 'user',)}),
        ('Token details', {'fields': ('social_access_token', 'social_token_type', 'social_expiry_date',)}),
    )
    search_fields = ('user',)
    filter_horizontal = ()

    def has_add_permission(self, request):
        return False

admin.site.register(SocialConnect, SocialConnectAdmin)
