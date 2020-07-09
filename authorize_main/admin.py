from django.contrib import admin
from .models import Account;
from django.contrib.auth.admin import UserAdmin;
# Register your models here.

class AccountAdmin(UserAdmin):
  list_display = ('email','date_joined','last_login','is_admin','is_staff','profile_pic','first_name','last_name',"id","show_to_public", "chat_keys")
  search_fields =('email','first_name','last_name')
  readonly_fields = ('date_joined','last_login')
  list_filter = ('email','first_name','last_name',)
  filter_horizontal = ()
  fieldsets = ()
  ordering = ('profile_pic', 'email', 'first_name', 'last_name', 'university', 'major', 'school_year', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', "chat_keys")

admin.site.register(Account,AccountAdmin)
