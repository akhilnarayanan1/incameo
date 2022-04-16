from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.conf import settings

def CustomExceptionHandler(exc, context):
    response = exception_handler(exc, context)
    return response

class NonFieldError(ValidationError):
  def __init__(self, error):
    return super().__init__({settings.NON_FIELD_ERRORS_KEY: error})

class MessageResponse(Response):
  def __init__(self, response, status=None):
    return super().__init__({"message": response}, status=status)