from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      path('home/', views.PostList, name='hometemplate'),
      path('create_post/', views.create_post_view, name='createposts'),
      path('make_bookmark/<int:post_id>/', views.make_bookmark, name='bookmark'),
      path('getbookmarkinfo_allposts/<int:post_id>/<int:page_number>/', views.getbookmarkinfo_allposts, name='getbookmarkinfo_allposts'),
      
      path('all_posts/',views.PostList,name="postlist"),
      path('bookmarked_posts/', views.BookmarkList, name='bookmarklist'),
      path('my_posts/', views.MyPostList, name='mypostlist'),
      path('my_posts/<int:post_id>/<int:page_number>/',views.MyPostList,name='mypostlist'),
      path('my_applied_posts/', views.ApplyList, name='applylist'),
      
      #path('apply', views.apply_view, name='apply'),
      #path('apply_all_post/', views.redir_2_all_post, name='applyall'),
      path('apply_all_post/<int:page_number>/', views.redir_2_all_post, name='applyall'),
      path('apply_bookmarks/<int:page_number>/', views.redir_2_bookmarked, name='applybookmark'),
      path('apply_bookmarks/', views.redir_2_bookmarked, name='applybookmark'),
      path('apply_form/<int:page_number>/', views.apply_page, name='applyform'),
      path('apply_form/', views.apply_page, name='applyform'),
      path('submit_application/<int:post_id>/<int:page_number>/', views.submit_application, name='submitapp'),
      
      path('delete_bookmark/<int:bookmark_id>/<int:page_number>/', views.delete_my_bookmark, name='delete_my_bookmark'),
      #path('delete_my_post/<int:post_id>/', views.delete_my_post, name='delete_my_post'),
      path('delete_my_post/<int:post_id>/<int:page_number>/', views.delete_my_post, name='delete_my_post'),
      
      path('edit_my_post/', views.edit_my_post, name ='edit_post'),
      
      path('applicant_profile/<int:user_id>/', views.applicant_profile, name='applicant_profile'),
      path('applicant_profile/', views.applicant_profile, name='applicant_profile'),
      path('accept_applicant/', views.accept_applicant, name='accept_applicant'),
      path('accept_applicant/<int:page_num>/', views.accept_applicant, name='accept_applicant'),     
      path('submit_filter_all/', views.filter_keyword_all, name='submit_filter_all'),
      path('submit_filter_applied/', views.filter_keyword_applied, name='submit_filter_applied'),
      path('submit_filter_bookmarked/', views.filter_keyword_bookmarked, name='submit_filter_bookmarked'),
      path('submit_filter_mypost/', views.filter_keyword_mypost, name='filter_keyword_mypost'),
      
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)