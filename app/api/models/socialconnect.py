from django.db import models
from api.models import User

class SocialConnect(models.Model):
    user = models.ForeignKey(
        'User',
        verbose_name='User',
        on_delete=models.CASCADE
    )
    access_token = models.TextField()
    expiry_date = models.DateTimeField()
    token_type = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user)