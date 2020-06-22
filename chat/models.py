from django.db import models
from django.contrib.postgres.fields.array import ArrayField
from authorize_main.models import Account
from posts_app.models import PostModel

# Create your models here.
class ChatModel(models.Model):
    users = ArrayField(models.IntegerField(), default=list,blank=True)
    owner = models.IntegerField(default = -1) 
    url = models.TextField(blank=True, max_length=50)
    key = models.BigIntegerField(blank=False, default=0)
    chat_name = models.CharField(max_length=50, blank=True, default='Chat')
    messages = ArrayField(models.TextField(), default=[])
