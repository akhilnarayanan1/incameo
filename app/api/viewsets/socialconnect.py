from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from api.permissions import IsOwnerAndAuthenticated
from api.models import SocialConnect
from api.serializers import CreateAccountSerializer, SocialConnectSerializer
from django.utils.timezone import now, timedelta
import requests
import json
import os

User = get_user_model()

class InstagramSocialConnectViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
    mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerAndAuthenticated,)
    queryset = SocialConnect.objects.all() 
    serializer_class = SocialConnectSerializer 

    def list(self, request, *args, **kwargs):
        response = super().list(self, request, *args, **kwargs)
        code = request.GET.get('code', None)
        if  code is None:
            return Response({"details": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        data = {
            "client_id": os.environ["client_id"],
            "client_secret": os.environ["client_secret"],
            "grant_type": "authorization_code",
            "redirect_uri": request.build_absolute_uri('/')[:-1]+"/api/instagram-verify/",
            "code": code
        }
        short_lived_resp = requests.post('https://api.instagram.com/oauth/access_token', data=data, verify=False)
        response = short_lived_resp

        access_token = short_lived_resp.json().get('access_token', None)
        if access_token is None:
            return Response({"details": short_lived_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        long_lived_resp = requests.get(f'https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={os.environ["client_secret"]}&access_token={access_token}', verify=False)

        access_token = long_lived_resp.json().get('access_token', None)
        if access_token is None:
            return Response({"details": long_lived_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        user_details_resp = requests.get(f'https://graph.instagram.com/v12.0/me?fields=account_type,id,media_count,username&access_token={access_token}', verify=False)
        response = user_details_resp

        obj, created = SocialConnect.objects.update_or_create(
            user=request.user,
            social_userid = user_details_resp.json().get('id', None),
            defaults={'social_expiry_date': now()}
        )

        obj.social_account_type = user_details_resp.json().get('account_type', None)
        obj.social_media_count = user_details_resp.json().get('media_count', 0)
        obj.social_username = user_details_resp.json().get('username', None)
        obj.social_access_token = access_token
        obj.social_expiry_date += timedelta(seconds=long_lived_resp.json().get('expires_in', 0))
        obj.social_token_type = long_lived_resp.json().get('token_type', None)
        obj.save()

        return Response({"details": response.json()}, status=status.HTTP_200_OK)
        
class FacebookSocialConnectViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
    mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerAndAuthenticated,)
    queryset = SocialConnect.objects.all() 
    serializer_class = SocialConnectSerializer 

    def list(self, request, *args, **kwargs):
        response = super().list(self, request, *args, **kwargs)
        code = request.GET.get('code', None)

        if code is None:
            return Response({"details": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f'https://graph.facebook.com/v12.0/oauth/access_token?client_id={os.environ["fb_client_id"]}&redirect_uri={request.build_absolute_uri("/")[:-1]+"/api/facebook-verify/"}&client_secret={os.environ["fb_client_secret"]}&code={code}', verify=False)

        return Response(response.json(), status=status.HTTP_200_OK)

