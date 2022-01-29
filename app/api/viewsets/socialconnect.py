from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from api.serializers import CreateAccountSerializer
import requests
import json
from pathlib import Path
import dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

User = get_user_model()

class ProcessInstagramCodeViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
  permission_classes = (AllowAny,)
  queryset = User.objects.all() 
  serializer_class = CreateAccountSerializer 

  def list(self, request, *args, **kwargs):
    response = super().list(self, request, *args, **kwargs)
    code = request.GET.get('code', None)
    if code:
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
        if access_token:
            long_lived_resp = requests.get(f'https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={os.environ["client_secret"]}&access_token={access_token}', verify=False)
            response = long_lived_resp

        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        return Response({"details": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)
