from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('logout/confirm', LogoutConfirmTemplateView.as_view(), name="logout_confirm"),
    path('profile/', ProfileTemplateView.as_view(), name="profile"),
    path('profile/update/',ProfileUpdateView.as_view(), name="profile_update"),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('email/sent/', EmailSentView.as_view(), name='email_sent'),
    path('email/confirm/<str:uidb64>/<str:token>/', ConfirmFromEmailView.as_view(), name='confirm_from_email'),
    path('email/confirm/success/', EmailConfirmSuccessView.as_view(), name="email_confirmed_success"),
    path('email/confirm/failed/', EmailConfirmFailedView.as_view(), name="email_confirmed_failed"),

    path('password/reset/', PasswordResetFormView.as_view(), name="password_reset"),
    path('password/reset/sent/', ResetEmailSentTemplateView.as_view(), name="reset_email_sent"),
    path('password/reset/confirm/<str:uidb64>/<str:token>/',
         EmailConfirmResetView.as_view(),
         name="email_confirm_reset"),
    path('password/reset/success/', ResetSuccessTemplateView.as_view(), name="reset_success"),
    path('password/reset/failed/old_link/', ResetFailedOldLinkTemplateView.as_view(), name="reset_failed_old_link"),


]

