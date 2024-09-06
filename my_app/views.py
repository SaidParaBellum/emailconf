import random
import string

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, TemplateView

from my_app.forms import RegisterForm, EmailForm, PasswordResetForm
from my_app.models import EmailConfirmation
from my_app.templatetags.filters import mask_email


# Create your views here.

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = 'login.html'


class CodeView(FormView):
    form_class = EmailForm
    template_name = 'send_code.html'
    success_url = reverse_lazy('send_code')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        code = str(random.randint(100000, 999999))
        EmailConfirmation.objects.update_or_create(email=email, defaults={'code': code})

        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return super().form_valid(form)

class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user


class ForgotPasswordView(FormView):
    form_class = PasswordResetForm
    template_name = 'forgot_password.html'
    success_url = reverse_lazy('password_reset_done')

    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            new_password = self.generate_random_password()
            user.set_password(new_password)
            user.save()

            send_mail(
                'Новый пароль',
                f'Ваш новый пароль: {new_password}',
                'asaidansor@gmail.com',
                [email],
                fail_silently=False,
            )

            masked_email = mask_email(email)
            return self.render_to_response(self.get_context_data(email=masked_email))
        except User.DoesNotExist:
            return self.form_invalid(form)


class PasswordResetDoneView(TemplateView):
    template_name = 'password_reset_done.html'