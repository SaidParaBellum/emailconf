from django import forms
from rest_framework.authtoken.admin import User

from my_app.models import EmailConfirmation


class RegisterForm(forms.ModelForm):
    confirmation_code = forms.CharField(max_length=6, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_confirmation_code(self):
        code = self.cleaned_data.get('confirmation_code')
        email = self.cleaned_data.get('email')
        if not EmailConfirmation.objects.filter(email=email, code=code).exists():
            raise forms.ValidationError("Неверный код подтверждения.")
        return code

class EmailForm(forms.Form):
    email = forms.EmailField()

class PasswordResetForm(forms.Form):
    email = forms.EmailField()