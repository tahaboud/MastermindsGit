from django.urls import path
from .views import PostCreateView, PostDeleteView, PostDetailView, PostUpdateView

app_name="posts"

urlpatterns = [
    path("create_post/", PostCreateView.as_view(), name="create"),
    path("<pk>/post-delete/", PostDeleteView.as_view(), name="delete"),
    path("<pk>/post-detail/", PostDetailView.as_view(), name="detail"),
    path("<pk>/post-update/", PostUpdateView.as_view(), name="update"),
]
