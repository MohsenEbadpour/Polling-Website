from django.db import models
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.urls import reverse
from django.conf import settings 


# Create your models here.
USERS_TYPE = (
            ('M','Manager'),
            ('D','Deputy'),
            ('S','Student'),
            ('P','Parent'),
            )



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email Address', unique=True)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    is_active = models.BooleanField('Active', default=True)
    user_type = models.CharField('User Type',choices=USERS_TYPE,max_length=1)
    national_id = models.BigIntegerField('National ID')
    full_name = models.CharField('Full Name',max_length=50,default="Undefined")
    objects = UserManager()
    is_staff = models.BooleanField('Staff Status',default=False)    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_name(self):
        full_name = '%s' % (self.full_name)
        return full_name.strip()

    def get_url(self):
        return reverse("accounts:home")
        
    def __str__(self):
        return self.full_name
    


class Notification(models.Model):
    title = models.CharField('Title',max_length=50)
    context = models.TextField('Context')
    date_time = models.DateTimeField('Date Created', auto_now_add=True)
    def __str__(self):
        return self.title
