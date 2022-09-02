# from curses.ascii import US
from datetime import date, datetime
import json
import re
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from .models import Message, User, Class, ClassMember
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django import forms
# Create your views here.

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['pic']

class UserImageDisplay(DetailView):
    model = User
    template_name = 'layout.html'
    context_object_name = 'user'

def index(request):
    return render(request, "fitnessWeb/index.html")

def landing_page(request):
    return render(request, "fitnessWeb/landing_page.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("classes"))
        else:
            return render(request, "fitnessWeb/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "fitnessWeb/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("landing"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "fitnessWeb/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "fitnessWeb/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("classes"))
    else:
        return render(request, "fitnessWeb/register.html")

def classes(request):
    all_classes = Class.objects.all()
    if(request.user.role == "member"):
        user_classes = request.user.classes.all()
        user_classes2 = []
        for item in user_classes:
            user_classes2.append(item.gym_class)
        available_classes = []
        for item in all_classes:
            if item not in user_classes2:
                available_classes.append(item)
        return render(request, "fitnessWeb/classes.html", {
            "user_classes" : user_classes,
            "available_classes": available_classes
        })
    else:
        instructor_name = request.user.username
        instructor_classes = []
        for item in all_classes:
            if item.instructor == instructor_name:
                instructor_classes.append(item)
        return render(request, "fitnessWeb/instructor_classes.html", {
            "user_classes" : instructor_classes
        })

def sign_up(request, class_id):
    if request.method == "POST":
        desired_class = Class.objects.get(pk = class_id)
        ClassMember.objects.create(user = request.user, gym_class = desired_class)
        return HttpResponseRedirect(reverse("classes"))
    else:
        return render(request, "fitnessWeb/index.html")

def messages(request):
    all_classes = Class.objects.all()
    if(request.user.role == "member"):
        user_classes = request.user.classes.all()
        instructors = []
        for item in user_classes:
            instructors.append(item.gym_class.instructor)
        return render(request, "fitnessWeb/messages.html", {
            "instructors": instructors
        })
    else:
        instructor_name = request.user.username
        instructor_classes = []
        for item in all_classes:
            if item.instructor == instructor_name:
                instructor_classes.append(item)
        members = []
        for item in instructor_classes:
            print(item.members.all())
            members.append(item.members.all())
        members2 = []
        for memberSet in members:
            for member in memberSet:
                members2.append(member.user.username)

        return render(request, "fitnessWeb/messages.html", {
            "instructors": members2
        })

def my_info(request, username):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    return render(request, "fitnessWeb/my_info.html", {
        "user": user,
        "form": form
    })

def get_messages(request, user):
    try:
        chat_user = User.objects.get_by_natural_key(user)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Query for requested post
    try:
        messages = Message.objects.filter(sender = request.user, user = chat_user) | Message.objects.filter(sender = chat_user, user = request.user)
        ordered_messages = messages.order_by('timestamp')
    except Message.DoesNotExist:
        return JsonResponse({"error": "Messages not found."}, status=404)

    if request.method == "GET":
        return JsonResponse([message.serialize() for message in ordered_messages], safe=False) 

@csrf_exempt
def create_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    value = data.get("value", "")
    username = data.get("user", "")
    try:
        user = User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
            return JsonResponse({"error": "User you are trying to send to does not exist"}, status=400)
    # timeStamp = "" + date.today().strftime("%B %d, %Y") + ", " + datetime.today().strftime("%I:%M %p")
    Message.objects.create(user=user, sender=request.user, value=value)
    return JsonResponse(value, safe=False)    