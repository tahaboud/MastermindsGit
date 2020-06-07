from django.urls import path
from appfive.views import index, register, user_login

app_name = "appfive"

urlpatterns = [
    path("register/", register, name = "register"),
    path("user_login/", user_login, name="user_login")
]
