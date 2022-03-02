from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.viewsets import (
    CreateAccountViewset, VerifyViewset, 
    ForgotViewset, EditProfileViewset, CustomTokenObtainPairView, InstagramConnectViewset,
    FacebookSocialConnectViewset, InstagramFacebookMapViewset, 
    ProfileMetricsViewset, ClickMetricsViewset, AudienceMetricsViewset
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()
router.register('signup', CreateAccountViewset, basename='auth_signup')
router.register('account/verify', VerifyViewset, basename='auth_verify')
router.register('account/forgot', ForgotViewset, basename='auth_forgot')
router.register('editprofile', EditProfileViewset, basename='auth_editprofile')
router.register('instagram-verify', InstagramConnectViewset, basename='auth_instagram')
router.register('facebook-verify', FacebookSocialConnectViewset, basename='auth_facebook')
router.register('instagram-facebook-map', InstagramFacebookMapViewset, basename='map_insta_fb')
router.register('metrics/profile', ProfileMetricsViewset, basename='metrics_profile')
router.register('metrics/clicks', ClickMetricsViewset, basename='metrics_clicks')
router.register('metrics/audience', AudienceMetricsViewset, basename='metrics_clicks')

urlpatterns = [
    path('', include(router.urls)),

    path('account/token/get/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]