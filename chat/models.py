from django.db import models
from django.contrib.postgres.fields.array import ArrayField
from authorize_main.models import Account
from posts_app.models import PostModel

# Create your models here.
class ChatModel(models.Model):
    users = ArrayField(models.IntegerField(), default=list,blank=True)
    key = models.BigIntegerField(blank=False, default=0)
    title = models.CharField(max_length=50, blank=False, default='Title')
    messages = ArrayField(models.TextField(), default=list, blank=True)


