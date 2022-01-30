from django.contrib import admin
from api.models import InstagramAccount

class InstagramAccountAdmin(admin.ModelAdmin):
    readonly_fields = ('userid', 'account_type', 'media_count', 'username', 
        'user', 'access_token', 'token_type', 'expiry_date',)
    list_display = ('user',)
    list_filter = ('user',)
    fieldsets = (
        ('User details', {'fields': ('userid', 'account_type', 'media_count', 'username', 'user',)}),
        ('Token details', {'fields': ('access_token', 'token_type', 'expiry_date',)}),
    )
    search_fields = ('user',)
    filter_horizontal = ()

    def has_add_permission(self, request):
        return False

admin.site.register(InstagramAccount, InstagramAccountAdmin)
