from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout, update_session_auth_hash
from authorize_main.forms import RegistrationForm, LogInForm
from posts_app.models import PostModel
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from authorize_main.models import Account
from Notifications.views import Notifications
from chat.views import list_all_people

def landing_page_view(request):
  if request.user.is_authenticated:
    return render(request,'authorize_main/landing_page.html',{"all_notifications":Notifications(request), 'friends': list_all_people()})
  else:
    return render(request,'authorize_main/landing_page.html',{})
   
  
def logout_view(request):
  logout(request)
  messages.success(request,'You have successfully logged out.')
  return redirect('landing_page')


def login_view(request): #Signs user in
  if request.POST:
      form = LogInForm(request.POST)
      email = request.POST['email']
      password = request.POST['password']
      
  
      user = authenticate(request, email=email, password=password)
      
      if user is not None:
        login(request,user)
        messages.success(request,'Welcome, ' + user.first_name + '! You have successfully logged in.')
        return redirect('hometemplate')
        
      else:
        badform = True
        messages.success(request,'Please fill out the fields correctly!')
        return render(request,"authorize_main/login_page.html", {"form":form,"badform":badform})
  
  else:
    form = LogInForm()
    messages.success(request,'Please fill out the fields correctly!') 
  return render(request,'authorize_main/login_page.html',{"form":form})


def registration_view(request): #validates and creates USer Model
  if request.POST:
    form = RegistrationForm(request.POST)
    
    if form.is_valid():
      form.save()
      email = form.cleaned_data.get('email')
      raw_password = form.cleaned_data.get('password1')
      account = authenticate(email=email,password=raw_password)
      login(request,account)
      messages.success(request,'Successfully registered as user')
      return redirect('hometemplate')
      
    else:
      print(form.errors)
      messages.warning(request,"Registration Failed")
      return render(request,'authorize_main/register_page.html')
  
  else:
    form = RegistrationForm()
  return render(request,'authorize_main/register_page.html',{"registration_form":form})


@login_required
def profile_view(request): #see private profile with friend list
  user = Account.objects.get(id=request.user.id)
  friend_list = []
  user_settings = user.show_to_public
  
  for friend_id in user.friends:
    friend = Account.objects.get(id=friend_id)
    friend_list.append(friend)
  
  return render(request,'authorize_main/new_profile.html', {'friend_list': friend_list,'profile_pic': user_settings[0], 'email': user_settings[1],'first_name': user_settings[2], 'last_name': user_settings[3],'university': user_settings[4], 'major': user_settings[5],'school_year': user_settings[6], 'date_joined': user_settings[7],"all_notifications":Notifications(request)})
 
@login_required 
def edit_profile(request): #edit provate profile
  if request.POST:

    user = Account.objects.get(id=request.user.id)
    user.email = request.POST['email']
    
    if request.FILES.get('img'):
      user.profile_pic = request.FILES.get('img')
      
    user.university = request.POST['university']
    user.major = request.POST['major']
    user.school_year = request.POST['school_year']
    user.bio = request.POST['bio']
    user.save()

    
    if request.POST.get('display_profile') == "1":
      user.show_to_public[0] = True
      user.save()
    else:
      user.show_to_public[0] = False
      user.save()
      
    if request.POST.get('display_email') == '1':
      user.show_to_public[1] = True
      user.save()
    else:
      user.show_to_public[1] = False
      user.save()
    
    # if request.POST.get('display_university') == '1':
    #   user.show_to_public[4] = True
    #   user.save()
    # else:
    #   user.show_to_public[4] = False
    #   user.save()
      
    # if request.POST.get('display_major') == '1':
    #   user.show_to_public[5] = True
    #   user.save()
    # else:
    #   user.show_to_public[5] = False
    #   user.save()

    # if request.POST.get('display_school_year') == '1':
    #   user.show_to_public[6] = True
    #   user.save()
    # else:
    #   user.show_to_public[6] = False
    #   user.save()
    
    messages.success(request,'Profile Updated')
  
    return redirect('profile')
  else:
    messages.success(request,'Error')
   
    return redirect('profile')  

def list_all_people():
    all_people = Account.objects.all()
    return all_people

def mini_chat(request):

  pass