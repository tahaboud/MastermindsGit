from django import forms
from django.conf import settings
from django.core.mail import EmailMessage

class ContactForm(forms.Form):
    name = forms.CharField(min_length=4, max_length=20, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(min_length=10, max_length=15, required=False)
    content = forms.CharField(min_length=10, max_length=500, widget=forms.Textarea)

    def send_email(self):
        name = self.cleaned_data["name"]
        user_email = self.cleaned_data["email"]
        content = self.cleaned_data["content"]
        current_site = "127.0.0.1:8000"
        email_subject = "Contacted by {0} and his email is '{1}'".format(name, user_email)
        message = content
        mm_email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            )
        user_subject = "Thank you for contacting us"
        user_message = "Hello {0}. \n Thank you for contacting us, you will be contacted shortly by one of our staff about your message. \n Here is a copy of your message: \n {1}".format(name, content)
        user_email_message = EmailMessage(
            user_subject,
            user_message,
            settings.EMAIL_HOST_USER,
            [user_email],
            )
        mm_email_message.send(fail_silently=True)
        user_email_message.send(fail_silently=True)
