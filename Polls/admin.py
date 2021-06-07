from django.contrib import admin

# Register your models here.
from .models import Poll,Vote
class PollAdmin(admin.ModelAdmin):
    class Meta:
        model = Poll


class VoteAdmin(admin.ModelAdmin):
    class Meta:
        model = Vote


        
admin.site.register(Poll,PollAdmin)        
admin.site.register(Vote,VoteAdmin)

