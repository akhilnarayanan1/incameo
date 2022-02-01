from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, mixins, viewsets
from api.serializers import FacebookConnectSerializer
from api.permissions import IsOwnerAndAuthenticated
from api.models import FacebookAccount
from django.utils.timezone import now, timedelta, datetime
import time
import requests


class ListMetricsViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'business_id'
    permission_classes = (IsOwnerAndAuthenticated,)
    queryset = FacebookAccount.objects.all() 
    serializer_class = FacebookConnectSerializer 

    def retrieve(self, request, *args, **kwargs):
        respose = super().retrieve(self, request, *args, **kwargs)
        epoch_time = int(time.mktime(now().timetuple()))
        account = self.get_object()

        response = requests.get(f"https://graph.facebook.com/v12.0/{account.business_id}/insights?"
            f"metric=impressions,reach,profile_views,follower_count&period=day&"
            f"since={epoch_time - 86400*7}&until={epoch_time}&access_token={account.access_token}", 
        verify=False)

        return Response(response.json(), status=status.HTTP_200_OK)