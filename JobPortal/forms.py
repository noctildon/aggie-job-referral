from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class CandidateCreationForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150)
    name = forms.CharField(label='Your real name', min_length=2, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = Candidate
        fields = ('username', 'name', 'email', 'password1')

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username = username)
        if new.count():
            raise ValidationError("Username Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match")
        return password2

    def save(self):
        self.username_clean()
        self.email_clean()
        self.clean_password2()

        user = User.objects.create_user(
            self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        return user, self.cleaned_data['name']


class RecruiterCreationForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150)
    name = forms.CharField(label='Your real name', min_length=2, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    class Meta:
        model = Recruiter
        fields = ('username', 'name', 'email', 'password1')

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username = username)
        if new.count():
            raise ValidationError("Username Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match")
        return password2

    def save(self):
        self.username_clean()
        self.email_clean()
        self.clean_password2()

        user = User.objects.create_user(
            self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        return user, self.cleaned_data['name']


# Opening post form
class PostForm(ModelForm):
    class Meta:
        model = Opening
        fields = ("company", "job_title", "job_description")

    def save(self):
        return self.cleaned_data['company'], self.cleaned_data['job_title'], self.cleaned_data['job_description']


# Edit the opening
class EditForm(ModelForm):
    class Meta:
        model = Opening
        fields = ("company", "job_title", "job_description", "status")

    def save(self):
        return self.cleaned_data['company'], self.cleaned_data['job_title'], self.cleaned_data['job_description'], self.cleaned_data['status']


# Referral request form
class RequestForm(ModelForm):
    class Meta:
        model = Referral
        fields = ("app_info", "resume")

    def save(self):
        return self.cleaned_data['app_info'], self.cleaned_data['resume']


# For candidate
class DashboardFormCandidate(ModelForm):
    class Meta:
        model = Candidate
        fields = ("resume", "email", "email_notification")

    def save(self):
        return self.cleaned_data['resume'], self.cleaned_data['email'], self.cleaned_data['email_notification']


# For recruiter
class DashboardFormRecruiter(ModelForm):
    class Meta:
        model = Recruiter
        fields = ("email", "email_notification",)

    def save(self):
        return self.cleaned_data['email'], self.cleaned_data['email_notification']


# class PwdChangeForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ("password",)

#     def save(self):
#         return self.cleaned_data['email'], self.cleaned_data['email_notification']