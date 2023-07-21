from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Deposits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_account = models.CharField(max_length=255)
    value = models.IntegerField()
    bank = models.CharField(max_length=255, default='')
    reference = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
