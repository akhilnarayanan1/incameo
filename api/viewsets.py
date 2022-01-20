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


class VerifyViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
  permission_classes = (IsOwnerAndAuthenticated,)
  queryset = AllVerifyOrForgotToken.objects.all()
  serializer_class = VerifyOrForgotAccountSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return Response({"detail": "Token created successfully"}, status=status.HTTP_201_CREATED)
  
  def perform_create(self, serializer):
    return create_or_verify(serializer, 'verify')

class Forgotiewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
  permission_classes = (AllowAny,)
  queryset = AllVerifyOrForgotToken.objects.all()
  serializer_class = VerifyOrForgotAccountSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return Response({"detail": "Token created successfully"}, status=status.HTTP_201_CREATED)
  
  def perform_create(self, serializer):
    return create_or_verify(serializer, 'verify')
    


def create_or_verify(serializer, token_type):
  if token_type != 'verify' or token_type != 'forgot':
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


# class VerifyViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
#   permission_classes = (IsOwnerAndAuthenticated,)
#   queryset = AllVerifyOrForgotToken.objects.all()
#   serializer_class = VerifyOrForgotAccountSerializer

#   def perform_create(self, serializer):
#     user=serializer.validated_data['user']
#     try:
#       user = User.objects.get(email=user)
#       available_token = AllVerifyOrForgotToken.objects.get(
#         user=user, 
#         token_type='verify', 
#         token_expiry__gt=now()
#       )
#       raise APIException('Token already exists')
#     except User.DoesNotExist:
#       raise APIException('User doesn\'t exist')
#     except AllVerifyOrForgotToken.DoesNotExist:
#       serializer.save(user=user, token_type='verify')