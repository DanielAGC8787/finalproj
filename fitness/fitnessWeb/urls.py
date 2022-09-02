from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("home", views.index, name="index"), 
    path("classes", views.classes, name="classes"),
    path("sign_up<int:class_id>", views.sign_up, name="sign_up"),
    path("messages", views.messages, name="messages"),
    path("users/<str:username>", views.my_info, name="my_info"),

    #API Routes
    path("get_messages/<str:user>", views.get_messages, name="get_messages"),
    path("create_message", views.create_message, name="create_message")
]
