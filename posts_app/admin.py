from django.contrib import admin
from .models import PostModel, BookmarkedModel, AppliedPostsModel

# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
  list_display = ('title_of_post','post_made_by','date_created','genres','post_made_by_id','id','applicants','accepted_applicants', 'application_deadline')
  search_fields = ('title_of_post','post_made_by','date_created','genres',)
  readonly_fields = ('date_created',)

class BookmarkAdmin(admin.ModelAdmin):
  list_display = ('account', 'account_id', 'bookmarked_post', 'bookmarked_post_id','days_left','get_application_deadline',)
  search_fields = ('account__email',)
  
  def get_application_deadline(self, object):
    return object.bookmarked_post.application_deadline

admin.site.register(BookmarkedModel,BookmarkAdmin)
admin.site.register(PostModel,PostModelAdmin)

class ApplyAdmin(admin.ModelAdmin):
  list_display = ('account', 'applied_post','accepted',)
  search_fields = ('account__email',)
  
admin.site.register(AppliedPostsModel, ApplyAdmin)