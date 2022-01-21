from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.viewsets import CreateAccountViewset, VerifyViewset, ForgotViewset, EditProfileViewset

router = DefaultRouter()
router.register('signup', CreateAccountViewset, basename='auth_signup')
router.register('account/verify', VerifyViewset, basename='auth_verify')
router.register('account/forgot', ForgotViewset, basename='auth_forgot')
router.register('editprofile', EditProfileViewset, basename='auth_editprofile')

urlpatterns = [
    path('', include(router.urls)),
]