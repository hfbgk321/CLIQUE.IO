from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields.array import ArrayField

# Create your models here.

class MyAccountManager(BaseUserManager):
  def create_user(self,email,first_name,last_name,university,major,school_year,password=None):
    if not email:
      raise ValueError("Users must have a email")
    user = self.model(
      email=self.normalize_email(email),
      first_name = first_name,
      last_name = last_name,
      university = university,
      major = major,
      school_year = school_year,
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self,email,password,first_name,last_name,university,major,school_year):
    user = self.create_user(
      email=self.normalize_email(email),
      password=password,
      first_name = first_name,
      last_name = last_name,
      university = university,
      major = major,
      school_year = school_year,
    )
    user.is_admin = True
    user.is_superuser = True
    user.is_staff = True
    user.save(using=self._db)
    return user

class Account(AbstractBaseUser):
  profile_pic = models.ImageField(upload_to='media',default ='/media/default_profile.png')
  email = models.EmailField(verbose_name="email", max_length=60,unique=True)
  first_name = models.CharField(verbose_name="first_name",max_length=20,blank=True)
  last_name = models.CharField(verbose_name="last_name",max_length=20,blank=True)
  bio = models.TextField(default='No Bio At The Moment')
  university = models.CharField(verbose_name="university",max_length = 1000,default ="")
  major = models.CharField(verbose_name="major",max_length=1000,default="")
  school_year = models.CharField(choices = (("1", "Freshman"),("2", "Sophomore"),("3", "Junior"),("4", "Senior"), ("5", "Other")),default="",max_length=1)
  chat_keys = ArrayField(models.BigIntegerField(), default=list, blank=True)
  friends = ArrayField(models.IntegerField(), default=list, blank=True)
  
  date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
  last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  
  show_to_public = ArrayField(models.BooleanField(), default=[True, True, True, True, True, True, True, True])
  #[profile_pic, email, first_name, last_name, university, major, school_year, date_joined]
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name','last_name','university','major','school_year']

  objects = MyAccountManager()

  def __str__(self):
    return self.email
  
  def has_perm(self,perm,obj=None):
    return self.is_admin
  
  def has_module_perms(self, app_label):
    return True


