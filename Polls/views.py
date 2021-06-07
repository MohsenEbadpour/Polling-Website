
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from Users.models import User, Notification
from .models import Vote, Poll
from Users.views import is_manager_or_deputy, is_int, is_student_or_parent,is_int


# Create your views here.
@login_required
def new_poll(request):
    if is_student_or_parent(request):
        return HttpResponseRedirect(reverse("Users:home"))

    if request.POST:
        if not("c1" in request.POST and "c2" in request.POST and "c3" in request.POST and "c4" in request.POST and "title" in request.POST and "context" in request.POST):
            messages.success(request, "Invalid Fields")
            return render(request, "Polls/form.html")
        poll = Poll(title=request.POST["title"],
                    context=request.POST["context"])
        if not("active" in request.POST):
            poll.is_active = False
        else:
            poll.is_active = True
        poll.choice_1 = request.POST["c1"]
        poll.choice_2 = request.POST["c2"]
        poll.choice_3 = request.POST["c3"]
        poll.choice_4 = request.POST["c4"]
        if "img" in request.FILES:
            poll.photo = request.FILES["img"]
        poll.save()
        messages.success(
            request, "The new poll created successfully: "+str(request.POST["title"]))
        return HttpResponseRedirect(reverse("Polls:list-manage"))

    return render(request, "Polls/form.html")


@login_required
def list_manage(request):
    if is_student_or_parent(request):
        return HttpResponseRedirect(reverse("Users:home"))

    polls = Poll.objects.all().order_by('-date_time')
    return render(request, "Polls/list-manage.html", {"polls": polls})


@login_required
def poll_delete(request, id_=None):
    if is_student_or_parent(request) or id_ is None:
        return HttpResponseRedirect(reverse("Users:home"))
    p = get_object_or_404(Poll, id=id_)
    t = p.title
    p.delete()
    messages.success(request,"The poll deleted successfully: "+t)
    return HttpResponseRedirect(reverse("Polls:list-manage"))


@login_required
def poll_detail(request, id_=None):
    if is_student_or_parent(request) or id_ is None:
        return HttpResponseRedirect(reverse("Users:home"))
    poll = get_object_or_404(Poll, id=id_)
    file_type = None
    if poll.photo:
        file_type = list((list(poll.photo.url.split("/"))[-1]).split("."))[-1]
        if "jpg" in file_type or "jpeg" in file_type or "jfif" in file_type or "pjpeg" in file_type or "pjp" in file_type or "png" in file_type or "svg" in file_type:
            file_type = "image"
        elif "mpg" in file_type or "mpeg" in file_type or "avi" in file_type or "wmv" in file_type or "mov" in file_type or "ogg" in file_type or "webm" in file_type or "mp4" in file_type:
            file_type = "video"
        else:
            file_type = None
    
    votes = Vote.objects.filter(poll=poll)
    A,B,C,D=0,0,0,0
    for v in votes:
        if v.choice == "A": A+=1;
        elif v.choice == "B": B+=1;
        elif v.choice == "C": C+=1;
        elif v.choice == "D": D+=1;

    return render(request, "Polls/poll-detail.html", {"poll": poll,"file_type":file_type,"votes":votes,"A":A,"B":B,"C":C,"D":D})


@login_required
def poll_edit(request, id_=None):
    if is_student_or_parent(request) or id_ is None:
        return HttpResponseRedirect(reverse("Users:home"))
    poll = get_object_or_404(Poll, id=id_)
    if request.POST:
        if not("c1" in request.POST and "c2" in request.POST and "c3" in request.POST and "c4" in request.POST and "title" in request.POST and "context" in request.POST):
            messages.success(request, "Invalid Fields")
            return render(request, "Polls/poll-edit.html", {"poll": poll})
        if not("active" in request.POST):
            poll.is_active = False
        else:
            poll.is_active = True
        poll.title = request.POST["title"]
        poll.context = request.POST["context"]
        poll.choice_1 = request.POST["c1"]
        poll.choice_2 = request.POST["c2"]
        poll.choice_3 = request.POST["c3"]
        poll.choice_4 = request.POST["c4"]
        if "img" in request.FILES:
            poll.photo = request.FILES["img"]
        poll.save()
        messages.success(
            request, "The poll edited successfully: "+str(request.POST["title"]))
        return HttpResponseRedirect(reverse("Polls:poll-detail", kwargs={"id_": poll.id}))

    return render(request, "Polls/poll-edit.html", {"poll": poll})

@login_required
def polls_history(request):
    if is_manager_or_deputy(request):
        return HttpResponseRedirect(reverse("Users:home"))
    votes = Vote.objects.filter(user=request.user).order_by("-date_time")

    return render(request, "Polls/history.html", {"votes": votes})

@login_required
def open_polls(request):
    if is_manager_or_deputy(request):
        return HttpResponseRedirect(reverse("Users:home"))
    
    if request.POST:
        if not("poll_id" in request.POST and "choice" in request.POST):
            messages.success(request, "Arguments are not valid!")
            return HttpResponseRedirect(reverse("Polls:open-polls"))

        if not(is_int(request.POST["poll_id"]) and request.POST["choice"] in ["A","B","C","D"]):
            messages.success(request, "Arguments are not valid!")
            return HttpResponseRedirect(reverse("Polls:open-polls"))

        poll = get_object_or_404(Poll, id=int(request.POST["poll_id"]))
        if poll :
            if not poll.is_active:
                messages.success(request, "Poll is not active to select!")
                return HttpResponseRedirect(reverse("Polls:open-polls"))

            vote = Vote.objects.filter(Q(poll=poll)&Q(user=request.user))
            if vote:
                messages.success(request, "You selected before!")
                return HttpResponseRedirect(reverse("Polls:open-polls"))
            else :
                vote = Vote(user=request.user,poll=poll,choice=request.POST["choice"])
                vote.save()
                messages.success(request, "Your choice submited!")
                return HttpResponseRedirect(reverse("Polls:open-polls"))
        else :
            messages.success(request, "The poll not found")
            return HttpResponseRedirect(reverse("Polls:open-polls"))

    else  :
        polls_ = Poll.objects.filter(Q(is_active=True)).order_by("-date_time")
        polls = []
        for poll in polls_ :
            votes = Vote.objects.filter(Q(poll=poll) & Q(user=request.user))
            if len(votes) == 0:
                file_type = None
                if poll.photo:
                    file_type = list((list(poll.photo.url.split("/"))[-1]).split("."))[-1]
                    if "jpg" in file_type or "jpeg" in file_type or "jfif" in file_type or "pjpeg" in file_type or "pjp" in file_type or "png" in file_type or "svg" in file_type:
                        file_type = "image"
                    elif "mpg" in file_type or "mpeg" in file_type or "avi" in file_type or "wmv" in file_type or "mov" in file_type or "ogg" in file_type or "webm" in file_type or "mp4" in file_type:
                        file_type = "video"
                    else:
                        file_type = None
                polls.append([poll,file_type])
        return render(request, "Polls/open-polls.html", {"polls": polls})


@login_required
def all_selections(request):
    if is_student_or_parent(request):
        return HttpResponseRedirect(reverse("Users:home"))

    votes = Vote.objects.all().order_by('-date_time')
    return render(request, "Polls/all-selections.html", {"votes": votes})
