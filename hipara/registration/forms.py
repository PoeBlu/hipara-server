from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(min_length=3, max_length=30, required=True)
    last_name = forms.CharField(min_length=3, max_length=30, required=True)
    username = forms.CharField(min_length=7, max_length=75, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=6, max_length=75)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError("This username already been Taken")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except:
            return email
        if user.metadata.deleted_at:
            raise forms.ValidationError("This Account is Disabled contact to Admin")
        raise forms.ValidationError("This email already been registered")

class SignUpForm(forms.Form):
    first_name = forms.CharField(min_length=3, max_length=30, required=True)
    last_name = forms.CharField(min_length=3, max_length=30, required=True)
    username = forms.CharField(min_length=7, max_length=75, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=6, max_length=75)
    job_title = forms.CharField(max_length=250, required=False)
    company = forms.CharField(max_length=250, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError("This username already been Taken")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except:
            return email
        if user.metadata.deleted_at:
            raise forms.ValidationError("This Account is Disabled contact to Admin")
        raise forms.ValidationError("This email already been registered")


class LoginForm(forms.Form):
    email = forms.CharField(required=True, min_length=7, max_length=75)
    password = forms.CharField(required=True, min_length=6, max_length=75)

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=6, max_length=75)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=6, max_length=75)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if self.user.check_password(old_password) :
            return old_password;
        raise forms.ValidationError("Old password isn't valid")

class UpdatePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=6, max_length=75)
    re_password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=6, max_length=75)

    def clean_re_password(self):
        password = self.cleaned_data['password']
        re_password = self.cleaned_data['re_password']
        if password == re_password:
            return re_password;
        raise forms.ValidationError("password and retyped password does not match")
