from rest_framework import serializers
from api.models import InstagramAccount

class InstagramConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramAccount
        fields = '__all__'