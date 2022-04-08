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
    # class Meta(UserCreationForm.Meta):
        model = Candidates
        # model = User
        fields = ('username', 'name', 'email', 'password1')
        # fields = UserCreationForm.Meta.fields + fields

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username = username)
        if new.count():
            raise ValidationError("User Already Exist")
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
            raise ValidationError("Password don't match")
        return password2

    def save(self):
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
            raise ValidationError("User Already Exist")
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
            raise ValidationError("Password don't match")
        return password2

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        return user, self.cleaned_data['name']


class PostForm(ModelForm):
    class Meta:
        model = Jobs
        fields = ("job_title", "company", "location")

    def save(self):
        return self.cleaned_data['job_title'], self.cleaned_data['company'], self.cleaned_data['location']

class ApplyForm(ModelForm):
    class Meta:
        model=Candidates
        fields=("name", "email")