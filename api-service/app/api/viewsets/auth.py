from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.functions import mask_email
from api.models import AllVerifyOrForgotToken
from api.permissions import IsOwnerAndAuthenticated
from api.serializers import (
  CreateAccountSerializer, VerifyOrForgotAccountSerializer, 
  EditProfileSerializer, ChangePasswordSerializer, CustomTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.timezone import now
from api.custom_response import NonFieldError, MessageResponse

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer

class CreateAccountViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
  permission_classes = (AllowAny,)
  queryset = User.objects.all() 
  serializer_class = CreateAccountSerializer 

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return MessageResponse("User created successfully", status=status.HTTP_201_CREATED)


class VerifyViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
                    viewsets.GenericViewSet):
  lookup_field = 'token'
  queryset = AllVerifyOrForgotToken.objects.all()
  serializer_class = VerifyOrForgotAccountSerializer

  def get_permissions(self):
    return [AllowAny()] if self.action == 'retrieve' else [IsOwnerAndAuthenticated()]

  def retrieve(self, request, *args, **kwargs):
    response = super().retrieve(request, *args, **kwargs)
    token = self.get_object()
    if token.token_type != 'verify':
      raise NonFieldError(['Invalid Token'])
    if token.token_expiry < now() or token.is_used:
      raise NonFieldError(['Token is expired or already used'])
    user = token.user
    if user.is_banned:
      raise NonFieldError(['This account is banned'])
    if user.is_verified:
      raise NonFieldError(['Account already verified'])
    user.is_verified = True
    user.save()
    token.is_used = True
    token.save()
    return MessageResponse("Account verified succesfully", status=status.HTTP_200_OK)

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return MessageResponse("Token created successfully", status=status.HTTP_201_CREATED)
  
  def perform_create(self, serializer):
    return create_or_verify(serializer, 'verify')

class ForgotViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
  lookup_field = 'token'
  permission_classes = (AllowAny,)
  queryset = AllVerifyOrForgotToken.objects.all()

  def get_serializer_class(self):
    if self.action == 'update':
      return ChangePasswordSerializer
    return VerifyOrForgotAccountSerializer

  def retrieve(self, request, *args, **kwargs):
    response = super().retrieve(request, *args, **kwargs)
    token = self.get_object()
    if token.token_type != 'forgot':
      raise NonFieldError(['Invalid Token'])
    if token.token_expiry < now() or token.is_used:
      raise NonFieldError(['Token is expired or already used'])
    user = token.user
    masked_email = mask_email(user.email)
    if user.is_banned:
      raise NonFieldError(['This account is banned'])
    return MessageResponse(f"Token verified succesfully for {masked_email}", status=status.HTTP_200_OK)

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return MessageResponse(f"Token created successfully", status=status.HTTP_201_CREATED)
  
  def perform_create(self, serializer):
    return create_or_verify(serializer, 'forgot')

  def update(self, request, *args, **kwargs):
    response = super().update(request, *args, **kwargs)
    token = self.get_object()
    token.is_used = True
    token.save()
    masked_email = mask_email(self.get_object().user.email)
    return MessageResponse(f"Password changed succesfully for {masked_email}", status=status.HTTP_200_OK)

  def perform_update(self, serializer):
    user = self.get_object().user
    user.set_password(serializer.validated_data['password'])
    user.save()
    serializer.save()


def create_or_verify(serializer, token_type):
  if token_type != 'verify' and token_type != 'forgot':
    raise NonFieldError(['Invalid token type'])
  user=serializer.validated_data['user']
  try:
    user = User.objects.get(email=user)
    if token_type == 'verify' and user.is_verified:
      raise NonFieldError(['User already verified'])
    available_token = AllVerifyOrForgotToken.objects.get(
      user=user, 
      token_type=token_type, 
      token_expiry__gt=now(),
      is_used=False
    )
    raise NonFieldError(['Token already exists'])
  except User.DoesNotExist:
    raise NonFieldError(['User doesn\'t exist'])
  except AllVerifyOrForgotToken.DoesNotExist:
    serializer.save(user=user, token_type=token_type)


class EditProfileViewset(mixins.UpdateModelMixin, viewsets.GenericViewSet):
  permission_classes = (IsOwnerAndAuthenticated,)
  queryset = User.objects.all()
  serializer_class = EditProfileSerializer

  def partial_update(self, request, *args, **kwargs):
    response = super().partial_update(request, *args, **kwargs)
    password = request.data.get('password', None)
    if password:
      user = self.get_object()
      user.set_password(password)
      user.save()
    return MessageResponse("Profile updated successfully", status=status.HTTP_200_OK)