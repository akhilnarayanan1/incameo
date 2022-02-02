from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from api.permissions import IsOwnerAndAuthenticated
from api.models import InstagramAccount, FacebookAccount
from api.serializers import (
    CreateAccountSerializer, InstagramConnectSerializer, 
    FacebookConnectSerializer, InstagramFacebookMapSerializer
)
from django.utils.timezone import now, timedelta
import requests
import json
import os

User = get_user_model()

class InstagramConnectViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
    mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerAndAuthenticated,)
    queryset = InstagramAccount.objects.all() 
    serializer_class = InstagramConnectSerializer 

    def list(self, request, *args, **kwargs):
        response = super().list(self, request, *args, **kwargs)
        code = request.GET.get('code', None)
        if  code is None:
            return Response({"message": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        data = {
            "client_id": os.environ["client_id"],
            "client_secret": os.environ["client_secret"],
            "grant_type": "authorization_code",
            "redirect_uri": request.build_absolute_uri('/')[:-1]+"/api/instagram-verify/",
            "code": code
        }
        short_lived_resp = requests.post('https://api.instagram.com/oauth/access_token', data=data)

        if short_lived_resp.status_code != status.HTTP_200_OK:
            return Response({"message": short_lived_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        long_lived_resp = requests.get(f"https://graph.instagram.com/access_token?"
            f"grant_type=ig_exchange_token&"
            f"client_secret={os.environ['client_secret']}&"
            f"access_token={short_lived_resp.json().get('access_token', None)}")

        if long_lived_resp.status_code != status.HTTP_200_OK:
            return Response({"message": long_lived_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        user_details_resp = requests.get(f"https://graph.instagram.com/v12.0/me?"
            f"fields=account_type,id,media_count,username&"
            f"access_token={long_lived_resp.json().get('access_token', None)}")

        if user_details_resp.status_code != status.HTTP_200_OK:
            return Response({"message": user_details_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        obj, created = InstagramAccount.objects.update_or_create(
            id = user_details_resp.json().get('id', None),
            defaults={'expiry_date': now()}
        )
        obj.user = request.user
        obj.account_type = user_details_resp.json().get('account_type', None)
        obj.media_count = user_details_resp.json().get('media_count', 0)
        obj.username = user_details_resp.json().get('username', None)
        obj.access_token = long_lived_resp.json().get('access_token', None)
        obj.expiry_date += timedelta(seconds=long_lived_resp.json().get('expires_in', 0))
        obj.token_type = long_lived_resp.json().get('token_type', None)
        obj.save()

        return Response({"message": "Account(s) added succesfully"}, status=status.HTTP_200_OK)
        
class FacebookSocialConnectViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
    mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerAndAuthenticated,)
    queryset = FacebookAccount.objects.all() 
    serializer_class = FacebookConnectSerializer 

    def list(self, request, *args, **kwargs):
        response = super().list(self, request, *args, **kwargs)
        code = request.GET.get('code', None)
        if code is None:
            return Response({"message": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        long_lived_resp = requests.get(f"https://graph.facebook.com/v12.0/oauth/access_token?"
            f"client_id={os.environ['fb_client_id']}&"
            f"redirect_uri={request.build_absolute_uri('/')[:-1]}/api/facebook-verify/&"
            f"client_secret={os.environ['fb_client_secret']}&"
            f"code={code}")

        if long_lived_resp.status_code != status.HTTP_200_OK:
            return Response({"message": long_lived_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        verify_permissions = requests.get(f"https://graph.facebook.com/v12.0/me/permissions?"
            f"access_token={long_lived_resp.json().get('access_token', None)}")

        for permission in verify_permissions.json().get('data', None):
            if ((permission['permission'] == 'email' or permission['permission'] == 'read_insights' or 
                permission['permission'] == 'pages_show_list' or permission['permission'] == 'instagram_basic' or
                permission['permission'] == 'instagram_manage_insights' or 
                permission['permission'] == 'pages_read_engagement' or permission['permission'] == 'public_profile') 
                and (permission['status'] == 'declined')):
                return Response({"message": permission['permission']+ " permissions missing"}, 
                status=status.HTTP_400_BAD_REQUEST)

        accounts_list_resp = requests.get(f"https://graph.facebook.com/v12.0/me/accounts?"+
            "fields=instagram_business_account{username,ig_id},access_token,name,category&"+
            f"access_token={long_lived_resp.json().get('access_token', None)}")

        account_list = accounts_list_resp.json().get('data', None)

        if account_list is None:
            return Response({"message": accounts_list_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        response = accounts_list_resp

        for account in account_list:
            if "instagram_business_account" in account:
                obj, created = FacebookAccount.objects.update_or_create(
                    id = account.get('id', None),
                    defaults={'expiry_date': now()}
                )
                obj.user = request.user
                obj.name = account.get('name', None)
                obj.business_id = account['instagram_business_account'].get('id', None)
                obj.ig_id = account['instagram_business_account'].get('ig_id', None)
                obj.username = account['instagram_business_account'].get('username', None)
                obj.token_type = long_lived_resp.json().get('token_type', None)
                obj.category = account.get('category', None)
                obj.access_token = account.get('access_token', None)
                obj.expiry_date += timedelta(seconds=long_lived_resp.json().get('expires_in', 0))
                obj.save()

        return Response({"message": "Account(s) added succesfully"}, status=status.HTTP_200_OK)


class InstagramFacebookMapViewset(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerAndAuthenticated,)
    queryset = InstagramAccount.objects.all() 
    serializer_class = InstagramFacebookMapSerializer 

