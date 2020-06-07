from django.shortcuts import render
from .forms import PostForm
from django.views import generic
from django.urls import reverse_lazy
from .models import PostModel
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from braces.views import SelectRelatedMixin
from django.http import JsonResponse

# Create your views here.
class PostCreateView(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    template_name = "posts/create_post.html"
    model = PostModel
    form_class = PostForm
    success_url = reverse_lazy("masterminds:home")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'msg': "success",
            }
            return JsonResponse(data)
        else:
            self.object = form.save(commit=False)
            self.object.creator = self.request.user
            self.object.save()
            return super().form_valid(form)


class PostListView(generic.ListView):
    template_name = "theSite/home.html"
    model = PostModel
    context_object_name = "posts"
    ordering = ["-creation_time"]


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    template_name = "posts/confirm-delete.html"
    model = PostModel
    success_url = reverse_lazy("masterminds:home")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.creator:
            return True
        return False

class PostDetailView(generic.DetailView):
    template_name = "posts/post-detail.html"
    model = PostModel

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = "posts/post-update.html"
    form_class = PostForm
    model = PostModel

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.creator:
            return True
        return False

    def get_success_url(self, **kwargs):
        post = self.get_object()
        return reverse_lazy("posts:detail", args=(post.pk,))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'msg': "success",
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)
