from django.urls import path, include, reverse
from web.views import IndexView, SignupView, LoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login')
]