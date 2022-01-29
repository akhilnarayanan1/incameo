from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from api.permissions import IsOwnerAndAuthenticated
from api.models import SocialConnect
from api.serializers import CreateAccountSerializer, SocialConnectSerializer
import requests
import json
import os

User = get_user_model()

class ProcessInstagramCodeViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
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
        return Response({"details": "Unable to get access_token"}, status=status.HTTP_400_BAD_REQUEST)
    
    long_lived_resp = requests.get(f'https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={os.environ["client_secret"]}&access_token={access_token}', verify=False)
    user_details_resp = requests.get(f'https://graph.instagram.com/v12.0/me?fields=account_type,id,media_count,username&access_token={long_lived_resp.json().get("access_token", None)}', verify=False)
    response = user_details_resp
    
    return Response(response.json(), status=status.HTTP_200_OK)
        

