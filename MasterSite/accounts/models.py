from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings

def upload_location(instance, filename):
    file_path = "accounts/{user_id}/{username}-{filename}".format(user_id=str(instance.id), username=str(instance.username), filename=filename)
    return file_path

class MyAccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, username, profile_pic, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            username = username,
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    profile_pic = models.ImageField(upload_to=upload_location, default="accounts/default/default.png", null=False, blank=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "profile_pic", "first_name", "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
    if instance.profile_pic.url == "/media/accounts/default/default.png":
        pass
    else:
        instance.profile_pic.delete(False)

# @receiver(post_save, sender=Account)
# def EmailVerification(sender, instance, created, *args, **kwargs):
#     if created:
#         print(instance)
#         current_site = "127.0.0.1:8000"
#         email_subject = "Activate your account"
#         message = render_to_string("accounts/email-message.html", {
#             "user": instance,
#             "domain": current_site,
#             "uid": urlsafe_base64_encode(force_bytes(instance.pk)),
#             "token": generate_token.make_token(instance),
#         })
#         email_message = EmailMessage(
#             email_subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [instance.email],
#              )
#         email_message.content_subtype = "html"
#         email_message.send(fail_silently=True)
