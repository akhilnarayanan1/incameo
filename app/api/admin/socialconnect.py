from django.contrib import admin
from api.models import SocialConnect

class SocialConnectAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'access_token', 'token_type', 'expiry_date',)
    list_display = ('user',)
    list_filter = ('user',)
    fieldsets = (
        ('User details', {'fields': ('user',)}),
        ('Token details', {'fields': ('access_token', 'token_type', 'expiry_date',)}),
    )
    search_fields = ('user',)
    filter_horizontal = ()

    def has_add_permission(self, request):
        return False

admin.site.register(SocialConnect, SocialConnectAdmin)
