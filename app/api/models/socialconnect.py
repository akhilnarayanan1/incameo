from django.db import models
from api.models import User

class InstagramAccount(models.Model):
    userid = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20)
    media_count = models.IntegerField(default=0)
    username = models.CharField(max_length=100)
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