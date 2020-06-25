from django.db import models
from authorize_main.models import Account
from datetime import datetime
from django.contrib.postgres.fields.array import ArrayField
# Create your models here.

class NotificationModel(models.Model):
  account = models.ForeignKey(Account,on_delete=models.CASCADE)
  notified_message = models.TextField(max_length=None)
  date_created = models.DateTimeField(auto_now=True)
  url = models.CharField(blank = True, max_length=100, default = '#')
  data = ArrayField(models.TextField(max_length=None), blank = True, default=list)

