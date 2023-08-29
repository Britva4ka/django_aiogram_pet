from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class SignUpForm(forms.Form):
    field_order = ['username', 'email', 'password', 'confirm_password']
    username = forms.CharField(label="Username", max_length=16, widget=forms.TextInput)
    password = forms.CharField(label="Password", max_length=32, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    confirm_password = forms.CharField(label="Confirm password", max_length=32, widget=forms.PasswordInput)

    def clean_username(self):
        username_form = self.cleaned_data.get('username')
        if not UserModel.objects.filter(username=username_form).exists():
            return username_form
        else:
            raise ValidationError("Username is already registered.")

    def clean_email(self):
        email_form = self.cleaned_data.get('email')
        if not UserModel.objects.filter(email=email_form).exists():
            return email_form
        else:
            self.add_error("email", "Email is already registered.")

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'Passwords do not match')

    def save(self):
        cleaned_data = self.cleaned_data
        del cleaned_data['confirm_password']
        return UserModel.objects.create_user(**cleaned_data)


class SignInForm(forms.Form):
    field_order = ['username', 'password']
    username = forms.CharField(label="Username", max_length=16, widget=forms.TextInput)
    password = forms.CharField(label="Password", max_length=32, widget=forms.PasswordInput)

    def clean(self):
        username_form = self.cleaned_data.get('username')
        password_form = self.cleaned_data.get('password')

        user = authenticate(username=username_form, password=password_form)
        if user is None:
            raise ValidationError("Invalid username or password.")

        return self.cleaned_data
