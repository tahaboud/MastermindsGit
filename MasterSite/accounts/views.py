from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AccountLogIn, AccountUpdateForm, PasswordResetForm
from django.contrib.auth import authenticate, login
from .models import Account
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from .mixins import AjaxableResponseMixin
from django.contrib.auth import views as auth_views


class SignUp(generic.CreateView):
    model = Account
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:thanks")
    template_name = "accounts/registration.html"

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        current_site = "127.0.0.1:8000"
        email_subject = "Activate your account"
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token.make_token(user)
        message = render_to_string("accounts/email-message.html", {
            "user": user.username,
            "domain": current_site,
            "uid": uid,
            "token": token,
        })
        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
             )
        email_message.content_subtype = "html"
        email_message.send(fail_silently=True)
        return response

class LoginView(generic.FormView):
    template_name = "accounts/login.html"
    form_class = AccountLogIn
    success_url = reverse_lazy("masterminds:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'msg': "Success",
            }
            return JsonResponse(data)
        email = self.request.POST["email"]
        password = self.request.POST["password"]
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

@login_required
def log_outView(request):
    logout(request)
    return redirect("masterminds:home")

class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    login_url = "/accounts/login"
    template_name = "accounts/account_update.html"
    fields = ["profile_pic", "email", "username", "first_name", "last_name"]
    success_url = reverse_lazy("masterminds:home")
    model = Account

    def test_func(self):
        account = self.get_object()
        if self.request.user == account:
            return True
        return False

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        return response

class AccountDetailView(generic.DetailView):
    template_name = "accounts/account_detail.html"
    model = Account

class AccountThankYouView(generic.TemplateView):
    template_name = "accounts/confirm_registration.html"

class AccountActivateView(generic.View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)

        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO, "account activated succefully")
            return redirect("accounts:success")

        return render(request, "accounts/activate_failed.html", status=401)

class AccountActivationSuccess(generic.TemplateView):
    template_name = "accounts/activation_success.html"

class PasswordResetView(auth_views.PasswordResetView):
    template_name = "accounts/reset_password.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("accounts:reset_email_sent")
    html_email_template_name = "accounts/reset_pass_email_msg.html"
    email_template_name = "accounts/reset_pass_email_msg.html"
    subject_template_name = "accounts/reset_subject.txt"

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'msg': "Success",
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)


class PasswordEmailSent(auth_views.PasswordResetDoneView):
    template_name = "accounts/reset_email_sent.html"

class CreateNewPassword(auth_views.PasswordResetConfirmView):
    template_name = "accounts/new_password.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'msg': "Success",
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)

class PasswordResetCompleted(auth_views.PasswordResetCompleteView):
    template_name = "accounts/reset_complete.html"
