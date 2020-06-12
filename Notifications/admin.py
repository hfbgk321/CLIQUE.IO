from django.contrib import admin
from Notifications.models import NotificationModel
# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
  list_display=('account','notified_message','date_created',)
  search_fields=('account__email',)

admin.site.register(NotificationModel,NotificationAdmin)
