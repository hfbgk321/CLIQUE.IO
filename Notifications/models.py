from django.db import models
from authorize_main.models import Account
from datetime import datetime
# Create your models here.

class NotificationModel(models.Model):
  account = models.ForeignKey(Account,on_delete=models.CASCADE)
  notified_message = models.TextField(max_length=None)
  date_created = models.DateTimeField(auto_now=True)

