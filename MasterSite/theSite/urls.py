from django.urls import path
from . import views
from posts import views as postViews

app_name = "masterminds"

urlpatterns = [
    path("", postViews.PostListView.as_view(), name="home"),
    path("coming-soon/", views.ComingSoonView.as_view(), name="comingsoon"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("thanks/", views.ThankContactView.as_view(), name="thanks"),
]
