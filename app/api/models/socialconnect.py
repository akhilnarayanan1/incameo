from django.db import models
from api.models import User

class SocialConnect(models.Model):
    social_userid = models.CharField(max_length=100)
    social_account_type = models.CharField(max_length=20)
    social_media_count = models.IntegerField(default=0)
    social_username = models.CharField(max_length=100)
    user = models.ForeignKey(
        'User',
        verbose_name='User',
        on_delete=models.CASCADE
    )
    social_access_token = models.TextField()
    social_expiry_date = models.DateTimeField()
    social_token_type = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user)