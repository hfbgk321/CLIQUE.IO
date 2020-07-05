from django.db import models
from authorize_main.models import Account
from django.utils import timezone
from django.contrib.postgres.fields.array import ArrayField
from django.conf import settings
import datetime

# Create your models here.

class PostModel(models.Model):
  title_of_post = models.CharField(max_length=100)
  description_of_post = models.TextField(max_length=None)
  post_made_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  date_created = models.DateTimeField(verbose_name="date published", auto_now_add=True)
  application_deadline = models.DateField(verbose_name = "Application Deadline", auto_now=False,auto_now_add=False,default = timezone.now)
  skills_needed = models.TextField(max_length=None, blank=True)
  num_of_positions = models.IntegerField(max_length=None)
  genres = ArrayField(models.CharField(max_length=50, blank=True), default=list)
  current_num_of_accepted_applicants = models.IntegerField(max_length=None,default=0)
  application_completed = models.BooleanField(default=False)
  applicants = ArrayField(models.IntegerField(),default=list,blank=True)
  accepted_applicants = ArrayField(models.IntegerField(), default=list,blank=True)
  application_questions = ArrayField(models.TextField(max_length=None, blank=True), default=list, blank=True)
  
  def __str__(self):
    return self.title_of_post

class AnswerModel(models.Model):
  applicant = models.ForeignKey(Account, on_delete = models.CASCADE)
  post = models.ForeignKey(PostModel, on_delete = models.CASCADE)
  answers = ArrayField(models.TextField(blank=True, default=""), default = list, blank=True)


class BookmarkedModel(models.Model):
  account = models.ForeignKey(Account,on_delete = models.CASCADE)
  bookmarked_post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
  days_left = models.IntegerField(default=3)
  
  
  def __str__(self):
    return self.account.first_name

class AppliedPostsModel(models.Model):
  account = models.ForeignKey(Account, on_delete = models.CASCADE)
  applied_post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
  accepted = models.BooleanField(default=False)
  
  def __str__(self):
      return self.account.first_name

