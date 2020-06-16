from django.shortcuts import render,reverse
from django.template import RequestContext
from .forms import PostForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from.models import PostModel, BookmarkedModel,AppliedPostsModel
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
import datetime
from authorize_main.models import Account
from Notifications.models import NotificationModel
from Notifications.views import Notifications
from newsapi import NewsApiClient

def getbookmarkinfo_allposts(request, post_id, page_number):
  return make_bookmark(request, post_id, page_number)
  #return HttpResponse(f'id:{post_id}, page_num: {page_number}')

def redir_2_all_post(request,page_number=1):
  #return HttpResponse(f'id:{post_id}, page_num: {page_number}')
  ret = apply_view(request)
  
  return redirect(f'/posts/all_posts/?page1={page_number}')

def redir_2_bookmarked(request, page_number=1):
  ret = apply_view(request)
  
  return redirect(f'/posts/bookmarked_posts/?page3={page_number}')

def apply_view(request):
  if request.POST:
    try:
        # for key, value in request.POST.items():
        #   print('Key:'+key+ ' Value:'+ value)
        # return HttpResponse('Hello')
        post_to_apply = request.POST['postID']
        #print(post_to_apply)
        user = request.user
        
        #expired_post_check = PostModel.objects.get(id=post_to_apply)
        #print(expired_post_check.application_completed)
          
        if PostModel.objects.get(id=post_to_apply).application_completed == True:
          return messages.success(request, 'Application has expired')
        
        already_applied_check = AppliedPostsModel.objects.filter(account__id = user.id, applied_post__id__contains = post_to_apply)

        if len(already_applied_check) > 0:
          return messages.success(request,'Post is already applied to!')
        else:
          raise ObjectDoesNotExist
    
    except ObjectDoesNotExist:  
      applied = AppliedPostsModel.objects.create(account=user,applied_post = PostModel.objects.get(id = post_to_apply))
      applied.id = post_to_apply
      current_post = PostModel.objects.get(id = post_to_apply)
      current_post.applicants.append(request.user.id)
      current_post.save()
      return messages.success(request,"Post Successfully Applied To")
  else:
    raise Exception('request is not POST')
   
def PostApplyList(request): #for poster to see which users applied
  apply_list = AppliedPostsModel.objects.all()
  users_applications = []
  for application in apply_list:
    if application.account.id == request.user.id:
      users_applications.append(apply_list)
  
  return render(request,'posts_app/Applied.html',{"users_applications":users_applications, 'all_notifications': Notifications(request)})

def PostList(request):
  postlist =AllAppliedBookmarkedView(request)[0]
  newsapi = NewsApiClient(api_key='2d6d2823f99f42aaa163e76c3dbb20fa')
  top_headlines = newsapi.get_top_headlines(language='en',sources='techcrunch')
  all_articles = top_headlines['articles']
  return render(request,'posts_app/home_template.html',{"pag_allposts":postlist, 'all_notifications': Notifications(request),"all_articles":all_articles})

def ApplyList(request): #for user to see which posts they applied to
  appliedposts_obj = AllAppliedBookmarkedView(request)[1]
  return render(request, 'posts_app/Applied.html', {'pag_appliedposts': appliedposts_obj, 'all_notifications': Notifications(request)})

def BookmarkList(request):
  bookmarks_obj = AllAppliedBookmarkedView(request)[2]
  return render(request,'posts_app/Bookmarked.html',{"pag_bookmarks":bookmarks_obj, 'all_notifications': Notifications(request)})

def MyPostList(request, post_id=None,page_number=1):
  mypost_obj = AllAppliedBookmarkedView(request,page_number)[3]
  #mypost_obj.number = page_number
  # print(page_number, mypost_obj.number, mypost_obj.paginator.num_pages)
  current_post = ''
  users = []
  accepted = []
  chat_url = []
  
  if post_id:
    post = PostModel.objects.get(id=post_id)
    applicants = post.applicants
    current_post = PostModel.objects.get(id=post_id).title_of_post
    
    for x in post.accepted_applicants:
      accepted.append(Account.objects.get(id=x)) 
    
    for x in post.applicants:
      users.append(Account.objects.get(id=x))
    #print(accepted)

    
    for x in range(len(accepted)):
      
      #print(request.user.id)
      #print(accepted[x].id)
      
      url = request.user.id + accepted[x].id * post.id 
    
      chat_url.append(url)
      
    user_url_combined = zip(accepted, chat_url)
    
  else:
    user_url_combined = []
    applicants = []

  return render(request, 'posts_app/My_Post.html', {"pag_mypost":mypost_obj, 'users': users,"current_post":current_post,
  "num":len(users),"post_id":post_id,"accepted":accepted,"num_accepted":len(accepted), 'all_notifications': Notifications(request),
  'user_url_combined': user_url_combined})
  
def AllAppliedBookmarkedView(request,page_number=None):
  all_posts = PostModel.objects.all()
  
  all_posts_filtered = []
  user_posts = []
  user_bookmarks = []
  applied_posts = []
  all_bookmarks = BookmarkedModel.objects.all()
  all_apps = AppliedPostsModel.objects.all()
  
  for book_mark in all_bookmarks:
    if book_mark.account.id == request.user.id:
      user_bookmarks.append(book_mark)
      deadline = book_mark.bookmarked_post.application_deadline
      if (datetime.date.today() + datetime.timedelta(days=3)) >= deadline and datetime.date.today() < deadline and book_mark.days_left == 3:
        NotificationModel.objects.create(account=request.user,notified_message =f'The post {book_mark.bookmarked_post.title_of_post} is about to expire in {book_mark.days_left} days. APPLY NOW!')   
        book_mark.days_left -= 1 
        book_mark.save()
      elif (datetime.date.today() + datetime.timedelta(days=2)) >= deadline and datetime.date.today() < deadline and book_mark.days_left == 2:
        NotificationModel.objects.create(account=request.user,notified_message =f'The post {book_mark.bookmarked_post.title_of_post} is about to expire in {book_mark.days_left} days. APPLY NOW!')   
        book_mark.days_left -= 1 
        book_mark.save()
      elif (datetime.date.today() + datetime.timedelta(days=1)) >= deadline and datetime.date.today() < deadline and book_mark.days_left == 1:
        NotificationModel.objects.create(account=request.user,notified_message =f'The post {book_mark.bookmarked_post.title_of_post} is about to expire in {book_mark.days_left} days. APPLY NOW!')   
        book_mark.days_left -= 1 
        book_mark.save()
      elif (datetime.date.today() + datetime.timedelta(days=1)) >= deadline and datetime.date.today() < deadline and book_mark.days_left == 0:
        NotificationModel.objects.create(account=request.user,notified_message =f'The post {book_mark.bookmarked_post.title_of_post} will expire tonight. Apply before 11:59pm!')   
        book_mark.days_left -= 1 
        book_mark.save()
        
  for post in all_posts:
    # print(type(post.application_deadline), type(datetime.date))
    if post.application_deadline <= datetime.date.today() or post.current_num_of_accepted_applicants == post.num_of_positions:
      post.application_completed = True
      post.save()
    else:
      post.application_completed = False
      post.save()
      
    if post.post_made_by.id == request.user.id:
      user_posts.append(post)
    else:
      if post.application_deadline > datetime.date.today() and post.current_num_of_accepted_applicants < post.num_of_positions:
        all_posts_filtered.append(post)
  
  for app_post in all_apps:
    if app_post.account.id == request.user.id:
      applied_posts.append(app_post)
  #print(applied_posts)
  paginator_allposts = Paginator(all_posts_filtered, 3)
  allposts_number = request.GET.get('page1',)
  allposts_obj = paginator_allposts.get_page(allposts_number)
  
  paginator_applied = Paginator(applied_posts, 3)
  app_posts_number = request.GET.get('page2')
  appliedposts_obj = paginator_applied.get_page(app_posts_number)
  
  paginator_bookmarks = Paginator(user_bookmarks, 3)
  bookmarks_number = request.GET.get('page3')
  bookmarks_obj = paginator_bookmarks.get_page(bookmarks_number)
  
  paginator_mypost = Paginator(user_posts, 3)
  mypost_number = request.GET.get('page4',page_number)
  mypost_obj = paginator_mypost.get_page(mypost_number)
  
  
  return [allposts_obj, appliedposts_obj, bookmarks_obj, mypost_obj]
  
  #return render(request,'posts_app/home_template.html',
                #{'pag_allposts': allposts_obj, 'pag_bookmarks': bookmarks_obj,"pag_mypost":mypost_obj})
    
@login_required
def create_post_view(request):
  if request.method == 'POST':
    form =PostForm(request.POST)
    if form.is_valid():
      title = request.POST['title_of_post']
      title = title.replace('\'','`')
      description = request.POST['description_of_post']
      description = description.replace('\'','`')
      description = description.replace('\n',' ').replace('\r','')
      post = form.save(commit = False)
      post.post_made_by = request.user
      post.title_of_post = title
      post.description_of_post = description
      post.save()
      messages.success(request,'Successfully created post.')
      return redirect('mypostlist')
    else:
      messages.warning(request,'Invalid post')
      return redirect('mypostlist')
  form = PostForm()
  return render(request,'posts_app/post_page.html',{"form":form, 'all_notifications': Notifications(request)}) 

def make_bookmark(request, post_id, page_number):
  try:
    post_to_bookmark = PostModel.objects.get(id=post_id)
    user = request.user
    in_favorite = BookmarkedModel.objects.filter(account__email__contains = user.email, bookmarked_post__id__contains = post_id)
    if len(in_favorite) > 0:
      for bookmark in in_favorite:
        bookmark.delete()
      messages.success(request,'Post Unbookmarked')
      return redirect(f'/posts/all_posts/?page1={page_number}')
    
    raise ObjectDoesNotExist
  except ObjectDoesNotExist:  
    bookmarked = BookmarkedModel.objects.create(account=user,bookmarked_post = post_to_bookmark)
    bookmarked.id = post_to_bookmark.id
    messages.success(request,"Post Sucessfully Bookmarked")
    return redirect(f'/posts/all_posts/?page1={page_number}')

def delete_my_bookmark(request, bookmark_id, page_number=1):
  bookmark = BookmarkedModel.objects.get(id=bookmark_id)
  bookmark.delete()
  messages.success(request,'Bookmark Deleted')
  return redirect(f'/posts/bookmarked_posts/?page3={page_number}')

def delete_my_post(request, post_id, page_number):
  print(page_number)
  my_post = PostModel.objects.get(id=post_id)
  my_post.delete()
  messages.success(request,'Post Deleted')
  return redirect(f'/posts/my_posts/?page4={page_number}')

def edit_my_post(request):
  if request.POST:
    # for key, value in request.POST.items():
    #     print('Key:'+key+ ' Value:'+ value)
    # return HttpResponse('Hello')
    
    my_post = PostModel.objects.get(id=request.POST['postID'])
    my_post.num_of_positions = request.POST['editMember']
    my_post.skills_needed = request.POST['editSkills']
    my_post.description_of_post = request.POST['editDescription']
    my_post.application_deadline = request.POST['editApplication_Deadline']
    my_post.save()
    messages.success(request,'Post Successfully Edited')
    return redirect('mypostlist')
  else:
    raise Exception('Request is not POST')

def applicant_profile(request, user_id):
  applicant = Account.objects.get(id=user_id)
  applicant_first_name = applicant.first_name
  settings = applicant.show_to_public
  if settings[0] == True and applicant.profile_pic != 'None':
    profile_pic = applicant.profile_pic.url
    print(applicant.profile_pic)
  else:
    profile_pic = '/media/media/default_profile.png'
  if settings[1] == True:
    email = applicant.email
  else:
    email = 'Not Visible To Public. Please Contact Through Chat.'
  #print(settings)
  #[profile_pic, email, first_name, last_name, university, major, school_year, date_joined]
  return render(request, 'posts_app/pub_profile.html', {'applicant':applicant, 'profile_pic': profile_pic, 'email': email, 'all_notifications': Notifications(request)})


def accept_applicant(request, page_num=1):
  accepted_ids = []
  if request.POST:
    accepted_applicants = request.POST['postIDapplicantID']
    post_id = int(request.POST['acceptPostID'])
    
    filtered_id = accepted_applicants.split()
    for x in filtered_id:
      accepted_ids.append(int(x))

    current_post = PostModel.objects.get(id=post_id)
    current_post.current_num_of_accepted_applicants += len(accepted_applicants)
    
    current_post.accepted_applicants.extend(accepted_ids)
    try:
      current_post.accepted_applicants.remove(' ')
    except:
      pass
    
    for x in accepted_ids:
      current_post.applicants.remove(x)
    current_post.save()

    for x in accepted_ids:
      all_applied = AppliedPostsModel.objects.get(account__id=x, applied_post__id = post_id)
      all_applied.accepted = True
      all_applied.save()
      recipient = Account.objects.get(id=x)
      NotificationModel.objects.create(account = recipient , notified_message = f'Congratulations! You have been accepted into {current_post.title_of_post}!')
      
    messages.success(request,'Successfully accepted applicants')
    return redirect(f'/posts/my_posts/{post_id}/{page_num}/?page4={page_num}')
    #return HttpResponse('Success')
  messages.warning(request, 'Failed to accept applicants')
  return redirect(f'/posts/my_posts/{post_id}/{page_num}/?page4={page_num}')
  #return HttpResponse('Failure')
        
