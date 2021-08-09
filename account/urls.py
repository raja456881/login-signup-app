from django.contrib import admin
from django.urls import path
from.views import *

urlpatterns = [
    path("signup", AccountSignupApiView.as_view(), name="account-signup"),
    path("login", AccountLoginApiView.as_view(), name="account-login"),
    path("", DoctorHomeApiView.as_view(), name="Doctor-home"),
    path("Patienthome", PatinentHomeApiView.as_view(), name="Patient-home" ),
    path("logout", handlelogout, name="logout"),
    path("doctor-blog", CreateBlogApiView.as_view()),
    path("list-blog", ShowBlogApiView.as_view()),
    path("draft", Draft.as_view())
]
