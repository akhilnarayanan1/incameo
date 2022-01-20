from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.viewsets import CreateAccountViewset, VerifyViewset, Forgotiewset

router = DefaultRouter()
router.register('signup', CreateAccountViewset, basename='auth_signup')
router.register('account/verify', VerifyViewset, basename='auth_verify')
router.register('account/forgot', Forgotiewset, basename='auth_forgot')

urlpatterns = [
    path('', include(router.urls)),
]