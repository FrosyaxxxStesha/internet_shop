from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms


User = get_user_model()


class RegistrationForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(auth_forms.AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProfileUpdateForm(auth_forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('avatar', 'telephone_number', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        del self.fields['password']


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autocomplete": "email"}))

    def clean_email(self):
        cleaned_data = self.cleaned_data.get("email")
        try:
            User.objects.get(email=cleaned_data)

        except User.DoesNotExist:
            raise forms.ValidationError("Пользователь с таким email не найден")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
