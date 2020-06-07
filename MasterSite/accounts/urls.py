from django.urls import path
from accounts import views as accntsViews
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("register/", accntsViews.SignUp.as_view(), name="register"),
    path("logout/", accntsViews.log_outView, name="logout"),
    path("login/", accntsViews.LoginView.as_view(), name="login"),
    path("update/<pk>/", accntsViews.AccountUpdateView.as_view(), name="update"),
    path("detail/<pk>/", accntsViews.AccountDetailView.as_view(), name="detail"),
    path("thank-you/", accntsViews.AccountThankYouView.as_view(), name="thanks"),
    path("activate/<uidb64>/<token>/", accntsViews.AccountActivateView.as_view(), name="activate"),
    path("activation-success/", accntsViews.AccountActivationSuccess.as_view(), name="success"),
    path("reset_password/", accntsViews.PasswordResetView.as_view(), name='password_reset'),
    path("reset_password_sent/", accntsViews.PasswordEmailSent.as_view(), name='reset_email_sent'),
    path("reset/<uidb64>/<token>/", accntsViews.CreateNewPassword.as_view(), name='password_reset_confirm'),
    path("reset_password_complete/", accntsViews.PasswordResetCompleted.as_view(), name='password_reset_complete'),
]
