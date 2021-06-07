from django.urls import path
from . import views

#from posts import views as ...
app_name = 'Polls'
urlpatterns = [
    path('new/', views.new_poll, name='new-poll'),
    path('list-manage/', views.list_manage, name='list-manage'),
    path('delete/<int:id_>', views.poll_delete, name='poll-delete'),
    path('detail/<int:id_>', views.poll_detail, name='poll-detail'),
    path('edit/<int:id_>', views.poll_edit, name='poll-edit'),
    path('my-history', views.polls_history, name='my-history'),
    path('open-polls', views.open_polls, name='open-polls'),
    path('all-selections', views.all_selections, name='all-selections'),

]
