from rest_framework import serializers
from api.models import InstagramAccount, FacebookAccount

class InstagramConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramAccount
        fields = '__all__'

class FacebookConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookAccount
        fields = '__all__'