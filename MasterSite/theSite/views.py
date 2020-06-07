from django.shortcuts import render
from .forms import ContactForm
from django.views import generic
from posts.models import PostModel
from .mixins import AjaxableResponseMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.http import HttpResponseRedirect

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "theSite/home.html"

class PostListView(generic.ListView):
    model = PostModel
    template_name = "theSite/home.html"

class ComingSoonView(generic.TemplateView):
    template_name = "theSite/coming_soon.html"

class AboutView(generic.TemplateView):
    template_name = "theSite/about.html"

class ContactView(generic.FormView):
    template_name = 'theSite/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("masterminds:thanks")

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
            form.send_email()
            return super().form_valid(form)

class ThankContactView(generic.TemplateView):
    template_name = "theSite/thanks-for-contacting.html"
