from .models import Account
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import authenticate
from django.conf import settings

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "username", "profile_pic", "password1", "password2"]

class AccountLogIn(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ["email", "password"]

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid email or password")

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["profile_pic", "email", "username"]

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            else:
                raise forms.ValidationError("Email '%s' is already in use." % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data["username"]
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            else:
                raise forms.ValidationError("Username '%s' is already in use." % username)

    def clean_profile_pic(self):
        if self.is_valid():
            profile_pic = self.cleaned_data["profile_pic"]
            return profile_pic

class PasswordResetForm(PasswordResetForm):

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                raise forms.ValidationError("We couldn't find a user with this email address")
            else:
                return email
