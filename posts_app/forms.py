from django import forms
from .models import PostModel


class PostForm(forms.ModelForm):
  class Meta:
    model = PostModel
    fields = ('title_of_post','description_of_post','skills_needed','num_of_positions','genres', 'application_deadline')
