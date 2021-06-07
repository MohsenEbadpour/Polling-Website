from django.db import models
from Users.models import User


CHOICES = (
            ('A','Choice #1'),
            ('B','Choice #2'),
            ('C','Choice #3'),
            ('D','Choice #4'),
            )

# Create your models here.
class Poll(models.Model):
    title = models.CharField('Title', max_length=50)
    context = models.TextField('Context')
    photo = models.FileField('Photo',upload_to='images/', blank=True)
    choice_1 = models.CharField('Choice #1', max_length=50)
    choice_2 = models.CharField('Choice #2', max_length=50)
    choice_3 = models.CharField('Choice #3', max_length=50)
    choice_4 = models.CharField('Choice #4', max_length=50)
    date_time = models.DateTimeField('Date Created', auto_now_add=True)
    is_active = models.BooleanField('Active', default=True)
    

    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    choice = models.CharField('Choise',choices=CHOICES,max_length=1)
    date_time = models.DateTimeField('Date Created', auto_now_add=True)
    def __str__(self):
        return str(self.poll.title) + " <=> " + str(self.user.full_name)



