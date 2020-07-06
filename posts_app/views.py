from django.shortcuts import render,reverse
from django.template import RequestContext
from .forms import PostForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from.models import PostModel, BookmarkedModel, AppliedPostsModel, AnswerModel
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
from chat.views import chat_key_seeder, create_private_chat, notify_chat, url_scrambler, list_all_people
from django.db.models.functions import Trunc
from friends.views import get_mutual_friends
import json
import urllib

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

def apply_page(request, page_number):
  post_id = request.POST['postID']
  post = PostModel.objects.get(id=post_id)
  question_num_lst= []
  
  if post.application_completed == True:
    return HttpResponse('This application has expired') 
  
  application_questions = post.application_questions
  for question in range(1, len(application_questions) + 1):
    question_num_lst.append(str(question))
  
  question_zip = zip(application_questions, question_num_lst)
  
  return render(request, "posts_app/application_questions.html", {'application_questions': question_zip, "post_id": post.id, "page_number":page_number}) 
  #return render(request, "", {"questions": questions})


def submit_application(request, post_id, page_number):
  print("answers----->", request.POST)
  user = Account.objects.get(id=request.user.id)
  post = PostModel.objects.get(id=post_id)
  
  if request.method == 'POST':

    questions = []
    answers = []
    
    if PostModel.objects.get(id=post_id).application_completed == True:
      messages.success(request, 'Application has expired')
      return redirect(f'/posts/all_posts/?page1={page_number}')

    for question_num in range(1, len(post.application_questions) + 1):
      answer = request.POST[str(question_num)]
      print("answer", answer)
      answers.append(answer)
      
    if len(AnswerModel.objects.filter(applicant=Account.objects.get(id=request.user.id), post=PostModel.objects.get(id=post_id))) == 0:
      apply_view(request, post_id)
      application = AnswerModel.objects.create(answers=answers, applicant=Account.objects.get(id=request.user.id), post=PostModel.objects.get(id=post_id))
      messages.success(request,"Application successfully submitted")
      return redirect(f'/posts/all_posts/?page1={page_number}')
    else:
      messages.success(request,"Application already submitted")
      return redirect(f'/posts/all_posts/?page1={page_number}') 
    
  messages.success(request,"Application failed")
  return redirect(f'/posts/all_posts/?page1={page_number}')


def apply_view(request, post_id):
  if request.POST:
    
    post_to_apply = post_id

    user = request.user
  
    applied = AppliedPostsModel.objects.create(account=user,applied_post = PostModel.objects.get(id = post_to_apply))
    applied.id = post_to_apply
    current_post = PostModel.objects.get(id = post_to_apply)
    current_post.applicants.append(request.user.id)
    current_post.save()
  
  else:
    raise Exception('request is not POST')
   
def PostApplyList(request): #for poster to see which users applied
  apply_list = AppliedPostsModel.objects.all()
  users_applications = []
  for application in apply_list:
    if application.account.id == request.user.id:
      users_applications.append(apply_list)
  
  return render(request,'posts_app/Applied.html',{"users_applications":users_applications, 'all_notifications': Notifications(request), 'friends':list_all_people()})

def PostList(request, searched=False, results=None, title='', sorted_option=''):
  
  if searched == False:
    postlist = AllAppliedBookmarkedView(request)[0]
  elif searched == True:
    
    paginator_allposts = Paginator(results, 3)
    allposts_number = request.GET.get('page1',1)
    postlist = paginator_allposts.get_page(allposts_number)
    
  newsapi = NewsApiClient(api_key='2d6d2823f99f42aaa163e76c3dbb20fa')
  top_headlines = newsapi.get_top_headlines(language='en',sources='techcrunch')
  all_articles = top_headlines['articles']

  for article in all_articles:
    clock = article['publishedAt']
    date = clock[0:10]
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]

    rearranged = month+'-'+day+'-'+year
    
    time = clock[11:int(len(clock)-4)]
    hours = time[0:2]
    minutes = time[3:5]
    am_or_pm=''
    if(int(hours) >= 12):
      am_or_pm = 'PM'
      hours = str(int(hours)-12)
    else:
      am_or_pm ='AM'
    
    article['publishedAt'] = rearranged+" "+ hours+":"+minutes+" "+am_or_pm
    
    
    
    # print(type(time))
    # print(time[0:10])
    # print(time[11:len(time)-1])
    # article['publishedAt'] = time[0:10]+" "+time[11:len(time)-1]
    # time = time[0,10] +" "+time[11,int(len(time))]

  
  
  #for post in PostModel.objects.all():
    #if post.application_completed is False:
      #print("post:", post.title_of_post, "Questions --->", post.application_questions)
  
    
  return render(request,'posts_app/home_template.html',{"pag_allposts":postlist, 'all_notifications': Notifications(request),"all_articles":all_articles, 'friends':list_all_people(), 'title': title, 'sorted_option':sorted_option})

def ApplyList(request, searched=False, results=None, title='', sorted_option=''): #for user to see which posts they applied to
  if searched == False:
    appliedposts_obj = AllAppliedBookmarkedView(request)[1]
    applied_posts_urls = AllAppliedBookmarkedView(request)[4]
  elif searched == True:
    
    paginator_allposts = Paginator(results, 3)
    allposts_number = request.GET.get('page2',1) 
    appliedposts_obj = paginator_allposts.get_page(allposts_number)
    urls = []
    for application in results:
      poster_id = application.applied_post.post_made_by.id
      post_id = application.applied_post.id
      if application.accepted:
        url =  url_scrambler(poster_id) + url_scrambler(post_id) + url_scrambler(request.user.id)
        
        urls.append(url)
      else:
        urls.append(0)
    applied_posts_urls = zip(appliedposts_obj, urls)
  return render(request, 'posts_app/Applied.html', {'pag_appliedposts': appliedposts_obj, 'applied_posts_urls': applied_posts_urls, 'all_notifications': Notifications(request), 'friends':list_all_people(), 'title': title, 'sorted_option':sorted_option})

def BookmarkList(request, searched=False, results=None, title='', sorted_option=''):
  if searched == False:
    
    bookmarks_obj = AllAppliedBookmarkedView(request)[2] 
  elif searched == True:
    
    paginator_bookmarks = Paginator(results, 3)
    bookmarks_number = request.GET.get('page3')
    bookmarks_obj = paginator_bookmarks.get_page(bookmarks_number)

  return render(request,'posts_app/Bookmarked.html',{"pag_bookmarks":bookmarks_obj, 'all_notifications': Notifications(request), 'friends':list_all_people(),'title': title, 'sorted_option':sorted_option})  

    
def MyPostList(request, post_id=None,page_number=1, searched=False, results=None, title='', sorted_option=''):
  
  if searched == False:
    mypost_obj = AllAppliedBookmarkedView(request,page_number)[3]
    #mypost_obj.number = page_number
    # print(page_number, mypost_obj.number, mypost_obj.paginator.num_pages)
    
      
  else:
    paginator_mypost = Paginator(results, 3)
    mypost_number = request.GET.get('page4',page_number)
    mypost_obj = paginator_mypost.get_page(mypost_number)
    
    
  current_post = ''
  users = []
  accepted = []
  chat_url = []
  user_apps = [] 
  if post_id:
    post = PostModel.objects.get(id=post_id)
    applicants = post.applicants
    current_post = PostModel.objects.get(id=post_id).title_of_post
    
    for x in post.accepted_applicants:
      accepted.append(Account.objects.get(id=x)) 
    
    for x in post.applicants:
      users.append(Account.objects.get(id=x))
    #print(accepted)

    user_url_combined = []
    
    for x in range(len(accepted)):
      questions = post.application_questions
      application = AnswerModel.objects.get(applicant=accepted[x], post=post) 
      answers = application.answers
      
      url = url_scrambler(request.user.id) + url_scrambler(post_id) + url_scrambler(accepted[x].id)
      create_private_chat(request, url, accepted[x].id)
      
      combined = [accepted[x], url, zip(questions, answers)]
      user_url_combined.append(combined)
      
      
  
    
    user_apps = []

    for user in range(len(users)):
      user = users[user]
      
      application = AnswerModel.objects.get(applicant=user, post=post)
      
      answers = application.answers
      questions = post.application_questions
      
      combined = [user, zip(questions, answers)]
      user_apps.append(combined)
    
  else:
    user_url_combined = []
    applicants = []
   
  
  return render(request, 'posts_app/My_Post.html', {"pag_mypost":mypost_obj, 'users': users,"current_post":current_post,
  "num":len(users),"post_id":post_id,"accepted":accepted,"num_accepted":len(accepted), 'all_notifications': Notifications(request),
  'user_url_combined': user_url_combined, 'friends':list_all_people(), 'title': title, 'sorted_option': sorted_option, "user_apps": user_apps})
  
def AllAppliedBookmarkedView(request,page_number=None):
  all_posts = PostModel.objects.all().order_by('id')
  all_posts_filtered = []
  user_posts = []
  user_bookmarks = []

  all_bookmarks = BookmarkedModel.objects.all().order_by('id') 
  applied_posts = AppliedPostsModel.objects.filter(account__id=request.user.id).order_by('id') 
  
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
       
  urls = []
  for application in applied_posts:
    if application.accepted == True:
      poster_id = application.applied_post.post_made_by.id
      post_id = application.applied_post.id
      url =  url_scrambler(poster_id) + url_scrambler(post_id) + url_scrambler(request.user.id)
      urls.append(url)

    else:
      urls.append(0)
  
  applied_posts_urls = zip(applied_posts, urls)
      
  #print(applied_posts)
  paginator_allposts = Paginator(all_posts_filtered, 3)
  allposts_number = request.GET.get('page1',)
  allposts_obj = paginator_allposts.get_page(allposts_number)
  
  paginator_applied = Paginator(applied_posts, 3)
  app_posts_number = request.GET.get('page2',)
  appliedposts_obj = paginator_applied.get_page(app_posts_number)
  
  paginator_bookmarks = Paginator(user_bookmarks, 3)
  bookmarks_number = request.GET.get('page3')
  bookmarks_obj = paginator_bookmarks.get_page(bookmarks_number)
  
  paginator_mypost = Paginator(user_posts, 3)
  mypost_number = request.GET.get('page4',page_number)
  mypost_obj = paginator_mypost.get_page(mypost_number)

  
  return [allposts_obj, appliedposts_obj, bookmarks_obj, mypost_obj, applied_posts_urls]
  
  #return render(request,'posts_app/home_template.html',
                #{'pag_allposts': allposts_obj, 'pag_bookmarks': bookmarks_obj,"pag_mypost":mypost_obj})
    
@login_required
def create_post_view(request):
  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      
      print("responses----->", request.POST)
      print("printing questions:")
      print("questions----->", request.POST.getlist('questions'), type(request.POST['questions']))
      
      title = request.POST['title_of_post']
      title = title.replace('\'','`')
      description = request.POST['description_of_post']
      description = description.replace('\'','`')
      description = description.replace('\n',' ').replace('\r','')
      post = form.save(commit = False)
      post.post_made_by = request.user
      post.title_of_post = title
      post.description_of_post = description
      post.application_questions = request.POST.getlist('questions')
      post.save()
      print("questions:::::::", post.application_questions)
      messages.success(request,'Successfully created post.')
      return redirect('mypostlist')
    else:
      messages.warning(request,'Invalid post')
      return redirect('mypostlist')
  form = PostForm()
  return render(request,'posts_app/post_page.html',{"form":form, 'all_notifications': Notifications(request), 'friends':list_all_people()}) 

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
  is_friend = False
  mutual_friends = get_mutual_friends(request)
  
  if user_id in Account.objects.get(id = request.user.id).friends:
    is_friend = True
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
  return render(request, 'posts_app/pub_profile.html', {'applicant':applicant, 'profile_pic': profile_pic, 'email': email, 'all_notifications': Notifications(request), 'friends':list_all_people(), 'is_friend': is_friend, 'common_friends':mutual_friends})


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



def filter_keyword_all(request):
  #obtain pagination info
  pre_url = request.build_absolute_uri().strip().split('&')
  print('pre_url------->', pre_url)
  
  #post request
  if len(pre_url) == 1:
    sorted_option = ''
    #keyword search
    title = request.POST.get('search')
    #interest search
    interest_lst = []
    
    interest_lst.append(request.POST.get('interestHealth'))
    interest_lst.append(request.POST.get('interestBusiness'))
    interest_lst.append(request.POST.get('interestArt'))
    interest_lst.append(request.POST.get('interestSoftware'))
    interest_lst.append(request.POST.get('interestData'))
    interest_lst.append(request.POST.get('interestWeb'))
    interest_text = (request.POST.get('moreInterests'))
    
    if interest_text is not None:
      interest_text = interest_text.strip().split(',')
      for word1 in interest_text:
        word = word1.strip()
        for word2 in word.split(' '):
          interest_lst.append(word2)
  
    #print('interest_lst------- ->', interest_lst)
    
    #sorted list
    sorted_lst = []
    
    sorted_lst.append(request.POST.get('upcomingDeadlines'))
    sorted_lst.append(request.POST.get(('mostRecent')))
    
    #print('sorted_list ---->', sorted_lst)
    
    #university = request.POST.get('university')
    
    #print('university ---->', university)
    
  else:
    sorted_option = pre_url[-1]
    sorted_lst = [pre_url[-1]]
    pre_url = pre_url[-2]
    title = pre_url
    interest_lst = []
    
  
  #print('sorted_option: >>>>>>>>>>>>>>', sorted_option, sorted_lst)
  #print('title: >>>>>>>>>>>>>>>>', title)
  relevant_lst = []
  filtered_list = []
  
  for interest in interest_lst:
    if interest != None:
      title = title + ',' + interest
  
  #if university is not '':
    #title = title + ',' + university
  
  if title is not None or title == '':
    
    keywords = title.strip().split(' ')
    for part in range(len(keywords)):
      filtered_list.extend(keywords[part].split(','))

    for ind in range(len(title)):
      if title[ind].isalnum() is not True:
        title = title.replace(title[ind], ',')
        
    print('title.>>>>>>>3', title)
    if title[-1] == ",":
      title = title[:-1]
    #print(title)
    
    if filtered_list[0] == '':
      filtered_list.pop(0)
    
    if filtered_list[-1] == "":
      filtered_list.pop()
    
    #print('filtered_lst-------->', filtered_list)
    
    #user_posts = PostModel.objects.filter(post_made_by__id=request.user.id)
    
    all_posts = PostModel.objects.all().order_by('id') 
    
    #search by filter
    for filter_option in sorted_lst:
      if filter_option is not None:
        if filter_option == 'upcomingDeadlines':
          sorted_option = 'upcomingDeadlines'
          all_posts = PostModel.objects.all().order_by('application_deadline').reverse()
          
        elif filter_option == 'mostRecent':
          sorted_option = 'date_created'
          all_posts = PostModel.objects.all().order_by('date_created').reverse()
      

    #search by keyword
    for word in filtered_list:
      word = word.strip()
      
      for post in all_posts:
        if post.post_made_by.id is not request.user.id and not post.application_completed:
        
          if word.lower() in post.title_of_post.lower():
            if post not in relevant_lst:
              relevant_lst.append(post)
          
          if word.lower() in post.description_of_post.lower():
            if post not in relevant_lst:
              relevant_lst.append(post)
          
          if word.lower() in post.skills_needed.lower():
            if post not in relevant_lst:
              relevant_lst.append(post)
          
          for genre in post.genres:
            if word.lower() == genre.lower():
              if post not in relevant_lst:
                relevant_lst.append(post)
              break
  
  #print(relevant_lst)
  if len(relevant_lst) == 0:
    messages.success(request,'No Post Relating to this Keyword')
    return redirect('hometemplate')
  return PostList(request, True, relevant_lst, title, sorted_option)



def filter_keyword_applied(request):
  #obtain pagination info
  pre_url = request.build_absolute_uri().strip().split('&')
  
  
  #post request
  if len(pre_url) == 1:
    sorted_option = ''
    #keyword search
    title = request.POST.get('search')
    
    #interest search
    interest_lst = []
    
    interest_lst.append(request.POST.get('interestHealth'))
    interest_lst.append(request.POST.get('interestBusiness'))
    interest_lst.append(request.POST.get('interestArt'))
    interest_lst.append(request.POST.get('interestSoftware'))
    interest_lst.append(request.POST.get('interestData'))
    interest_lst.append(request.POST.get('interestWeb'))
    interest_text = (request.POST.get('moreInterests'))
    
    if interest_text is not None:
      interest_text = interest_text.strip().split(',')
      for word1 in interest_text:
        word = word1.strip()
        for word2 in word.split(' '):
          interest_lst.append(word2)
  
    #print('interest_lst------- ->', interest_lst)
    
    #sorted list
    sorted_lst = []
    
    sorted_lst.append(request.POST.get('upcomingDeadlines'))
    sorted_lst.append(request.POST.get(('mostRecent')))
    
    #print('sorted_list ---->', sorted_lst)
    
    #university = request.POST.get('university')
    
    #print('university ---->', university)
    
  else:
    sorted_option = pre_url[-1]
    sorted_lst = [pre_url[-1]]
    pre_url = pre_url[-2]
    title = pre_url
    interest_lst = []
    

  relevant_lst = []
  filtered_list = []
  
  for interest in interest_lst:
    if interest != None:
      title = title + ',' + interest
  
  #if university is not '':
    #title = title + ',' + university
  
  if title is not None or title == '':
    
    keywords = title.strip().split(' ')
    for part in range(len(keywords)):
      filtered_list.extend(keywords[part].split(','))

    for ind in range(len(title)):
      if title[ind].isalnum() is not True:
        title = title.replace(title[ind], ',')
        
    #print(title)
    
    if filtered_list[0] == '':
      filtered_list.pop(0)
    
    if filtered_list[-1] == "":
      filtered_list.pop()
    
    #print('filtered_lst-------->', filtered_list)
    
    #user_posts = PostModel.objects.filter(post_made_by__id=request.user.id)
    
    all_posts = AppliedPostsModel.objects.filter(account__id=request.user.id).order_by('id') 
    
    #search by filter
    for filter_option in sorted_lst:
      if filter_option is not None:
        if filter_option == 'upcomingDeadlines':
          sorted_option = 'upcomingDeadlines'
          all_posts = AppliedPostsModel.objects.filter(account__id=request.user.id).order_by('applied_post__application_deadline').reverse()
        elif filter_option == 'mostRecent':
          sorted_option = 'date_created'
          all_posts = AppliedPostsModel.objects.filter(account__id=request.user.id).order_by('applied_post__date_created').reverse()
          

    #search by keyword
    for word in filtered_list:
      word = word.strip()
      
      for post in all_posts:
        
        if post.applied_post.post_made_by.id is not request.user.id:
          
          if word.lower() in post.applied_post.title_of_post.lower():
            if post not in relevant_lst:
              relevant_lst.append(post)
          
          if word.lower() in post.applied_post.description_of_post.lower():
            if post not in relevant_lst:
              relevant_lst.append(post)
          
          if word.lower() in post.applied_post.skills_needed.lower():
            if post not in relevant_lst:
              relevant_lst.append(post)
          
          for genre in post.applied_post.genres:
            if word.lower() == genre.lower():
              if post not in relevant_lst:
                relevant_lst.append(post)
              break
  #print(relevant_lst)
  if len(relevant_lst) == 0:
    messages.success(request,'No Post Relating to this Keyword')
    return redirect('applylist')
    #return PostList(request)
  return ApplyList(request, True, relevant_lst, title, sorted_option)


def filter_keyword_bookmarked(request):
  #obtain pagination info
  pre_url = request.build_absolute_uri().strip().split('&')
  
  
  #post request
  if len(pre_url) == 1:
    sorted_option = ''
    #keyword search
    title = request.POST.get('search')
    
    #interest search
    interest_lst = []
    
    interest_lst.append(request.POST.get('interestHealth'))
    interest_lst.append(request.POST.get('interestBusiness'))
    interest_lst.append(request.POST.get('interestArt'))
    interest_lst.append(request.POST.get('interestSoftware'))
    interest_lst.append(request.POST.get('interestData'))
    interest_lst.append(request.POST.get('interestWeb'))
    interest_text = (request.POST.get('moreInterests'))
    
    if interest_text is not None:
      interest_text = interest_text.strip().split(',')
      for word1 in interest_text:
        word = word1.strip()
        for word2 in word.split(' '):
          interest_lst.append(word2)
  
  
    sorted_lst = []
    
    sorted_lst.append(request.POST.get('upcomingDeadlines'))
    sorted_lst.append(request.POST.get(('mostRecent')))
    
    
    
  else:
    sorted_option = pre_url[-1]
    sorted_lst = [pre_url[-1]]
    pre_url = pre_url[-2]
    title = pre_url
    interest_lst = []
    
  

  relevant_lst = []
  filtered_list = []
  
  for interest in interest_lst:
    if interest != None:
      title = title + ',' + interest
  
  
  
  if title is not None or title == '':
    
    keywords = title.strip().split(' ')
    for part in range(len(keywords)):
      filtered_list.extend(keywords[part].split(','))

    for ind in range(len(title)):
      if title[ind].isalnum() is not True:
        title = title.replace(title[ind], ',')
        
    #print(title)
    
    if filtered_list[0] == '':
      filtered_list.pop(0)
    if filtered_list[-1] == "":
      filtered_list.pop()
    


    all_posts = BookmarkedModel.objects.filter(account__id=request.user.id).order_by('id') 
    
    #search by filter
    for filter_option in sorted_lst:
      if filter_option is not None:
        if filter_option == 'upcomingDeadlines':
          sorted_option = 'upcomingDeadlines'
          all_posts = BookmarkedModel.objects.filter(account__id=request.user.id).order_by('bookmarked_post__application_deadline').reverse()
        
        elif filter_option == 'mostRecent':
          sorted_option = 'date_created'
          all_posts = BookmarkedModel.objects.filter(account__id=request.user.id).order_by('bookmarked_post__date_created').reverse()
      

    #search by keyword
    for word in filtered_list:
      word = word.strip()
      
      for post in all_posts:
        
        if word.lower() in post.bookmarked_post.title_of_post.lower():
          if post not in relevant_lst:
            relevant_lst.append(post)
        
        if word.lower() in post.bookmarked_post.description_of_post.lower():
          if post not in relevant_lst:
            relevant_lst.append(post)
        
        if word.lower() in post.bookmarked_post.skills_needed.lower():
          if post not in relevant_lst:
            relevant_lst.append(post)
        
        for genre in post.bookmarked_post.genres:
          if word.lower() == genre.lower():
            if post not in relevant_lst:
              relevant_lst.append(post)
            break

  if len(relevant_lst) == 0:
    messages.success(request,'No Post Relating to this Keyword')
    return redirect('bookmarklist')
    #return PostList(request)
  return BookmarkList(request, True, relevant_lst, title, sorted_option)


def filter_keyword_mypost(request):
  #obtain pagination info
  pre_url = request.build_absolute_uri().strip().split('&')
  
  #post request
  if len(pre_url) == 1:
    sorted_option = ''
    #keyword search
    title = request.POST.get('search')
    
    #interest search
    interest_lst = []
    
    interest_lst.append(request.POST.get('interestHealth'))
    interest_lst.append(request.POST.get('interestBusiness'))
    interest_lst.append(request.POST.get('interestArt'))
    interest_lst.append(request.POST.get('interestSoftware'))
    interest_lst.append(request.POST.get('interestData'))
    interest_lst.append(request.POST.get('interestWeb'))
    interest_text = (request.POST.get('moreInterests'))
    
    if interest_text is not None:
      interest_text = interest_text.strip().split(',')
      for word1 in interest_text:
        word = word1.strip()
        for word2 in word.split(' '):
          interest_lst.append(word2)
  
    
    sorted_lst = []
    
    sorted_lst.append(request.POST.get('upcomingDeadlines'))
    sorted_lst.append(request.POST.get(('mostRecent')))
    
  
    
  else:
    sorted_option = pre_url[-1]
    sorted_lst = [pre_url[-1]]
    pre_url = pre_url[-2]
    title = pre_url
    interest_lst = []
  
  relevant_lst = []
  filtered_list = []
  
  for interest in interest_lst:
    if interest != None:
      title = title + ',' + interest
    
  if title is not None or title == '':
    
    keywords = title.strip().split(' ')
    for part in range(len(keywords)):
      filtered_list.extend(keywords[part].split(','))

    for ind in range(len(title)):
      if title[ind].isalnum() is not True:
        title = title.replace(title[ind], ',')
      
    if filtered_list[0] == '':
      filtered_list.pop(0)
    if filtered_list[-1] == "":
      filtered_list.pop()
    
    all_posts = PostModel.objects.filter(post_made_by__id=request.user.id).order_by('id') 
    
    #search by filter
    for filter_option in sorted_lst:
      if filter_option is not None:
        if filter_option == 'upcomingDeadlines':
          sorted_option = 'upcomingDeadlines'
          all_posts = PostModel.objects.filter(post_made_by__id=request.user.id).order_by('application_deadline').reverse()
          
        elif filter_option == 'mostRecent':
          sorted_option = 'date_created'
          all_posts = PostModel.objects.filter(post_made_by__id=request.user.id).order_by('date_created').reverse()
          
  
    #search by keyword
    for word in filtered_list:
      word = word.strip()
      
      for post in all_posts:
        
        if word.lower() in post.title_of_post.lower():
          if post not in relevant_lst:
            relevant_lst.append(post)
        
        if word.lower() in post.description_of_post.lower():
          if post not in relevant_lst:
            relevant_lst.append(post)
        
        if word.lower() in post.skills_needed.lower():
          if post not in relevant_lst:
            relevant_lst.append(post)
        
        for genre in post.genres:
          if word.lower() == genre.lower():
            if post not in relevant_lst:
              relevant_lst.append(post)
            break

  #print(relevant_lst)
  if len(relevant_lst) == 0:
    messages.success(request,'No Post Relating to this Keyword')
    return redirect('mypostlist')
    #return PostList(request)
  return MyPostList(request, None, 1, True, relevant_lst, title, sorted_option)

