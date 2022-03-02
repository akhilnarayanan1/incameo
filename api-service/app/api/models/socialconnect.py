from django.db import models
from api.models import User

class InstagramAccount(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
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
    facebook_linked = models.OneToOneField(
        'FacebookAccount',
        verbose_name='Facebook Account',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.username)


class FacebookAccount(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    business_id = models.CharField(max_length=100)
    ig_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    user = models.ForeignKey(
        'User',
        verbose_name='User',
        on_delete=models.CASCADE
    ) 
    category = models.CharField(max_length=100)
    access_token = models.TextField()
    expiry_date = models.DateTimeField()
    token_type = models.CharField(max_length=10)

    def __str__(self):
        return str(self.username)