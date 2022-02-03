from django.urls import path, include
from web.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]