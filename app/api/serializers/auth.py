from django.contrib.auth import get_user_model
from api.functions import get_device_details, token_generator
from api.models import AllVerifyOrForgotToken
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'id': self.user.userid})
        return data

class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields =  ('email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        request = self.context["request"]
        user = User.objects.create_user(**validated_data)
        AllVerifyOrForgotToken.objects.create(
            token=token_generator(32), 
            token_type='verify', 
            ip=request.META.get('REMOTE_ADDR', 'Unable to Fetch'),
            devicedetails=get_device_details(request.META.get('HTTP_USER_AGENT', 'Unable to Fetch')),
            user=user
        )
        return user

class VerifyOrForgotAccountSerializer(serializers.Serializer):
    user = serializers.EmailField()

    def create(self, validated_data):
        request = self.context["request"]
        token = AllVerifyOrForgotToken.objects.create(
            token=token_generator(32),
            ip=request.META.get('REMOTE_ADDR', 'Unable to Fetch'),
            devicedetails=get_device_details(request.META.get('HTTP_USER_AGENT', 'Unable to Fetch')),
            **validated_data
        )
        return token

class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password', 'date_of_birth', 'phone')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }