from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse



class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        form.send_email()
        return HttpResponseRedirect(reverse('masterminds:thanks'))
