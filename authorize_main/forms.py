from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authorize_main.models import Account

class RegistrationForm(UserCreationForm):
  class Meta:
    model = Account
    fields = ("email", "first_name", 
            "last_name", "university", 
            "major","school_year", 
            "password1","password2")

class LogInForm(forms.ModelForm):
  password = forms.CharField(label='Password', widget=forms.PasswordInput)

  class Meta:
    model = Account
    fields = ('email','password')
