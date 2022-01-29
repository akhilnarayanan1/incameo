from rest_framework import serializers
from api.models import SocialConnect

class SocialConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialConnect
        fields = '__all__'