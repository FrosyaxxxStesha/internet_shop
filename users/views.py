from django.views.generic import CreateView, View, TemplateView, UpdateView, FormView
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, PasswordResetForm
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, PasswordResetView


User = get_user_model()


# Регистрация


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/registration.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"url_name": "registration"}

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse('users:confirm_from_email', kwargs={'uidb64': uid, 'token': token})
        current_site = Site.objects.get_current().domain

        send_mail(
            'Подтвердите адрес электронной почты',
            f'Для окончания регистрации необходимо подтвердить вашу электронную почту.\
            Чтобы это сделать, перейдите по ссылке: http://{current_site}{activation_url}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return redirect('users:email_sent')


class ConfirmFromEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed_success')
        return redirect('users:email_confirmed_failed')


class EmailSentView(TemplateView):
    template_name = 'registration/email_sent.html'


class EmailConfirmSuccessView(TemplateView):
    template_name = 'registration/email_confirmed_success.html'


class EmailConfirmFailedView(TemplateView):
    template_name = 'registration/email_confirmed_failed.html'


# Вход и выход


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"url_name": "login"}


class LogoutConfirmTemplateView(TemplateView):
    template_name = "registration/logout_confirm.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"url_name": "logout"}


# Работа с профилем


class ProfileTemplateView(TemplateView):
    model = User
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"url_name": "profile"}


class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile_update.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs) | {"url_name": "profile"}

        if self.request.POST:
            context_data['form'] = ProfileUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context_data['form'] = ProfileUpdateForm(instance=self.request.user)
        return context_data

    def get_success_url(self):
        return reverse('users:profile')


# Сброс пароля


class PasswordResetFormView(FormView):
    form_class = PasswordResetForm
    template_name = "users/password_reset_form.html"

    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data['email'])
            if not user.is_active:
                raise User.DoesNotExist

        except User.DoesNotExist:
            user = None

        if user is not None:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_url = reverse('users:email_confirm_reset', kwargs={'uidb64': uid, 'token': token})
            current_site = Site.objects.get_current().domain
            send_mail(
                'Подтвердите смену пароля',
                f'Чтобы сбросить пароль, необходимо пройти по ссылке:\
                http://{current_site}{activation_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

            return redirect("users:reset_email_sent")

        # На всякий случай, в основе должна выскакивать ошибка в clean методе
        return redirect("users:reset_failed_no_user")


class EmailConfirmResetView(View):
    RESET_TOKEN_SESSION_KEY = 'password_reset_token'
    external_token = "reset_token"

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token == self.external_token:
            session_token = self.request.session[self.RESET_TOKEN_SESSION_KEY]
            if default_token_generator.check_token(user, session_token):
                new_password = User.objects.make_random_password(length=12)
                user.set_password(new_password)
                user.save()

                login(request, user)
                send_mail(
                    'Пароль успешно сброшен',
                    f'Пароль успешно сброшен, ваш новый пароль: {new_password}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
            return redirect('users:reset_success')

        elif user is not None and default_token_generator.check_token(user, token):
            self.request.session[self.RESET_TOKEN_SESSION_KEY] = token
            redirect_url = self.request.path.replace(token, self.external_token)
            return redirect(redirect_url)

        return redirect('users:reset_failed_old_link')


class ResetEmailSentTemplateView(TemplateView):
    template_name = "users/reset_email_sent.html"


class ResetFailedNoUserTemplateView(TemplateView):
    template_name = "users/reset_failed_no_user.html"


class ResetFailedOldLinkTemplateView(TemplateView):
    template_name = "users/reset_failed_old_link.html"


class ResetSuccessTemplateView(TemplateView):
    template_name = "users/reset_success.html"
