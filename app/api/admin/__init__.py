from django.contrib import admin
from .auth import *
from .socialconnect import *

admin.site.site_header = "InCAMEO Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to InCAMEO Admin Portal"