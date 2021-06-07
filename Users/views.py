
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .models import User,Notification
# Create your views here.
from Polls.models import Vote,Poll

def is_manager_or_deputy(request):
    if request.user.user_type == "M" or request.user.user_type == "D":
        return True 
    else :
        return False 

def is_student_or_parent(request):
    if request.user.user_type == "S" or request.user.user_type == "P":
        return True 
    else :
        return False 
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

@login_required
def home(request):
    if is_manager_or_deputy(request):
        len_users= len(User.objects.filter(Q(user_type="S") | Q(user_type="P")))
        len_votes = len(Vote.objects.all())
        len_polls = len(Poll.objects.all())
        
        if len_polls==0:
            notifications = Notification.objects.all().order_by('-date_time')
            empty = False
            if len(notifications) == 0:
                empty = True
            return render(request,'Users/home.html',{"notifications":notifications,"empty":empty,"is_sp":True})
        poll = Poll.objects.all().order_by('date_time').reverse()[0] 
        votes = Vote.objects.filter(poll=poll)
        A,B,C,D=0,0,0,0
        for v in votes:
            if v.choice == "A": A+=1;
            elif v.choice == "B": B+=1;
            elif v.choice == "C": C+=1;
            elif v.choice == "D": D+=1;
        file_type = None
        if poll.photo:
            file_type = list((list(poll.photo.url.split("/"))[-1]).split("."))[-1]
            if "jpg" in file_type or "jpeg" in file_type or "jfif" in file_type or "pjpeg" in file_type or "pjp" in file_type or "png" in file_type or "svg" in file_type:
                file_type = "image"
            elif "mpg" in file_type or "mpeg" in file_type or "avi" in file_type or "wmv" in file_type or "mov" in file_type or "ogg" in file_type or "webm" in file_type or "mp4" in file_type:
                file_type = "video"
            else:
                file_type = None

        return render(request,'Users/home.html',{"len_users":len_users,"len_votes":len_votes,"len_polls":len_polls,"poll":poll,"A":A,"B":B,"C":C,"D":D,"votes":votes,"file_type":file_type})
    else :
        notifications = Notification.objects.all().order_by('-date_time')
        empty = False
        if len(notifications) == 0:
            empty = True
        return render(request,'Users/home.html',{"notifications":notifications,"empty":empty,"is_sp":True})



def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Users:home"))
    if request.POST:
        if not ("email" in request.POST and "password" in request.POST ):
            messages.success(request, "Arguments are not valid!")
            return render(request,'Users/login.html')
        e = str(request.POST["email"]).lower()
        p = request.POST["password"]
        u = User.objects.filter(email=e)
        if len(u) !=1:
            messages.success(request, "With given email, user not found")
        else :
            u = u[0]
            if u.check_password(p):
                login(request,u)
                return HttpResponseRedirect(reverse("Users:home"))
            else:
                messages.success(request, "Password is incorrect")
    return render(request,'Users/login.html')

@login_required
def profile(request):
    return render(request,'Users/profile.html')

@login_required
def change_password(request):
    if request.POST:
        if not (("c_pass1" in request.POST) and ("n_pass1" in request.POST) and ("n_pass2" in request.POST)):
            messages.success(request, "Arguments are not valid!")
            return render(request,'Users/change-password.html')
        c_pass = str(request.POST["c_pass1"])
        if request.user.check_password(c_pass):
            if str(request.POST["n_pass1"]) == str(request.POST["n_pass2"]) and len(str(request.POST["n_pass1"]))>=4:
                request.user.set_password(request.POST["n_pass2"])
                request.user.save()
                messages.success(request, "Your password was changed!")
                return HttpResponseRedirect(reverse("Users:home"))
            else:
                messages.success(request, "Your new passwords are not valid or same!")
        else:
            messages.success(request, "Your old password entered wrong!")
       
    return render(request,'Users/change-password.html')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("Users:login"))



@login_required
def notification_new(request):
    if is_student_or_parent(request) :
        return HttpResponseRedirect(reverse("Users:home"))
    if request.POST:
        if not ("title" in request.POST and "context" in request.POST ):
                messages.success(request, "Arguments are not valid!")
                return render(request,"Users/notification-new.html")

        title = str(request.POST["title"])
        context = str(request.POST["context"])
        noti = Notification(title=title,context=context)
        noti.save()
        messages.success(request, "Notification was created!")
        return HttpResponseRedirect(reverse("Users:notification-list"))
    
    return render(request,"Users/notification-new.html")

@login_required
def notification_list(request):
    notifications = Notification.objects.all().order_by('-date_time')
    empty = False
    if len(notifications) == 0:
        empty = True
    return render(request,"Users/notification-list.html",{"notifications":notifications,"empty":empty})



@login_required
def delete_notification(request,id_=None):
    if is_student_or_parent(request) or id_ is None :
        return HttpResponseRedirect(reverse("Users:home"))
    noti = get_object_or_404(Notification,id=id_)
    t="The notification deleted successfully: "+noti.title
    messages.success(request,t)
    noti.delete()
    return HttpResponseRedirect(reverse("Users:notification-list"))


@login_required
def add_new_user(request):
    if is_student_or_parent(request) :
        return HttpResponseRedirect(reverse("Users:home"))
    if request.POST:
        if not ("email" in request.POST and "full_name" in request.POST and "password" in request.POST and "user_type" in request.POST and "national_id" in request.POST):
                messages.success(request, "Arguments are not valid!")
                return render(request,"Users/new-user.html")
        if request.POST["user_type"] != "S" and request.POST["user_type"] != "P" :
            messages.success(request, "You can only create student or parent!")
            return render(request,"Users/new-user.html")
        full_name = request.POST["full_name"]    
        user_type = request.POST["user_type"]
        email = request.POST["email"]
        found = User.objects.filter(email=email)
        if len(found)!=0:
            messages.success(request, "This email recorded before!")
            return render(request,"Users/new-user.html")
        password  = request.POST["password"]
        if len(password)<4:
            messages.success(request, "Password should be at least 4 char!")
            return render(request,"Users/new-user.html")
        
        if not(is_int(request.POST["national_id"])) or int(request.POST["national_id"])<0:
            messages.success(request, "National ID should be positive number!")
            return render(request,"Users/new-user.html")
            
        national_id = int(request.POST["national_id"])

        new_user = User(email=email,user_type=user_type,full_name=full_name,national_id=national_id)
        new_user.set_password(password)
        new_user.save()
        messages.success(request, "User Created!")
        return HttpResponseRedirect(reverse("Users:users-list"))

    user_ = "Student"
    if request.path != "/users/add-new-student":
        user_="Parent"
    return render(request,"Users/new-user.html",{"user_":user_})

@login_required
def users_list(request):
    if is_student_or_parent(request) :
        return HttpResponseRedirect(reverse("Users:home"))
    users= User.objects.filter(Q(user_type="S") | Q(user_type="P"))
    return render(request,"Users/users-list.html",{"users":users})


@login_required
def users_detail(request,id_=None):
    if is_student_or_parent(request) or id_ is None :
        return HttpResponseRedirect(reverse("Users:home"))
    user_ = get_object_or_404(User,id=id_)
    votes = Vote.objects.filter(user=user_)
    return render(request,"Users/user-detail.html",{"user_":user_,"votes":votes})

@login_required
def user_delete(request,id_=None):
    if is_student_or_parent(request) or id_ is None :
        return HttpResponseRedirect(reverse("Users:home"))
    user_ = get_object_or_404(User,id=id_)
    t = user_.full_name
    messages.success(request,"The user deleted successfully: "+t)
    user_.delete()
    return HttpResponseRedirect(reverse("Users:users-list"))

    
    
