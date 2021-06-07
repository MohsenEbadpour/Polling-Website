from django.urls import path
from . import views

#from posts import views as ...
app_name = 'Users'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('notification/new', views.notification_new, name='notification-new'),
    path('notification/list', views.notification_list, name='notification-list'),
    path('change-password/', views.change_password, name='change-password'),
    path('notification/delete/<int:id_>', views.delete_notification, name='delete-notification'),
    path('users/add-new-student', views.add_new_user, name='add-new-user'),
    path('users/add-new-parent', views.add_new_user, name='add-new-parent'),
    path('users/list', views.users_list, name='users-list'),
    path('users/detail/<int:id_>', views.users_detail, name='users-datail'),
    path('users/delete/<int:id_>', views.user_delete, name='user-delete'),
    path('', views.home, name='home'),
]
