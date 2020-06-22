from django.contrib import admin
from .models import ChatModel
# Register your models here.
# class ChatModel(models.Model):
#     users = ArrayField(models.IntegerField(), default=list,blank=True)
#     owner = models.IntegerField(default = -1) 
#     url = models.TextField(blank=True, max_length=50)
#     key = models.BigIntegerField(blank=False, default=0)
#     chat_name = models.CharField(max_length=50, blank=True, default='Chat')
#     messages = ArrayField(models.TextField(), default=[])


class ChatAdmin(admin.ModelAdmin):
  list_display =('users','owner','url','key','chat_name','messages',)

admin.site.register(ChatModel,ChatAdmin);