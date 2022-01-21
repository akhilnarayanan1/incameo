from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.exceptions import APIException, ValidationError, NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.functions import get_device_details, token_generator
from api.models import AllVerifyOrForgotToken
from api.permissions import IsOwnerAndAuthenticated
from api.serializers import CreateAccountSerializer, VerifyOrForgotAccountSerializer
from django.utils.timezone import now

User = get_user_model()

class CreateAccountViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
  permission_classes = (AllowAny,)
  queryset = User.objects.all() 
  serializer_class = CreateAccountSerializer 

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return Response({"detail": "User created successfully"}, status=status.HTTP_201_CREATED)


class VerifyViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
                    viewsets.GenericViewSet):
  lookup_field = 'token'
  queryset = AllVerifyOrForgotToken.objects.all()
  serializer_class = VerifyOrForgotAccountSerializer

  def get_permissions(self):
    return [AllowAny()] if self.action == 'retrieve' else [IsOwnerAndAuthenticated()]

  def retrieve(self, request, *args, **kwargs):
    response = super().retrieve(request, *args, **kwargs)
    token = AllVerifyOrForgotToken.objects.get(token=kwargs['token'])
    if token.token_expiry < now():
      raise ValidationError({"detail": "Token Expired"})
    user = token.user
    if user.is_banned:
      raise ValidationError({"detail": "User is banned"})
    if user.is_verified:
      raise ValidationError({"detail": "User already verified"})
    user.is_verified = True
    user.save()
    return Response({"detail": "Account verified succesfully"}, status=status.HTTP_200_OK)

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return Response({"detail": "Token created successfully"}, status=status.HTTP_201_CREATED)
  
  def perform_create(self, serializer):
    return create_or_verify(serializer, 'verify')

class ForgotViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
                    viewsets.GenericViewSet):
  lookup_field = 'token'
  permission_classes = (AllowAny,)
  queryset = AllVerifyOrForgotToken.objects.all()
  serializer_class = VerifyOrForgotAccountSerializer

  def retrieve(self, request, *args, **kwargs):
    response = super().retrieve(request, *args, **kwargs)
    token = AllVerifyOrForgotToken.objects.get(token=kwargs['token'])
    if token.token_expiry < now():
      raise ValidationError({"detail": "Token Expired"})
    user = token.user
    if user.is_banned:
      raise ValidationError({"detail": "User is banned"})
    return Response({"detail": "Token verified succesfully"}, status=status.HTTP_200_OK)

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return Response({"detail": "Token created successfully"}, status=status.HTTP_201_CREATED)
  
  def perform_create(self, serializer):
    return create_or_verify(serializer, 'forgot')
    


def create_or_verify(serializer, token_type):
  if token_type != 'verify' and token_type != 'forgot':
    raise APIException('Invalid token type')
  user=serializer.validated_data['user']
  try:
    user = User.objects.get(email=user)
    available_token = AllVerifyOrForgotToken.objects.get(
      user=user, 
      token_type=token_type, 
      token_expiry__gt=now()
    )
    raise APIException('Token already exists')
  except User.DoesNotExist:
    raise APIException('User doesn\'t exist')
  except AllVerifyOrForgotToken.DoesNotExist:
    serializer.save(user=user, token_type=token_type)
