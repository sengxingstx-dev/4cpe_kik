from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, ScoreDetail



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'gender', 'dob', 'village', 'district', 'province',
            'nationality', 'tribe', 'phone', 'degree', 'position'
        ]  # Update with the desired fields from your UserProfile model


class RegistrationForm(UserCreationForm):
    # by default UserCreationForm provided only: usrername, password1, password2
    # to include email field to a form
    email = forms.EmailField(max_length=100, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # form validations
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            # check if we find that user 
            # user = User.objects.get(username=username)
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in use.')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            # user = User.objects.get(email=email)
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use.')


class ScoreDetailForm(forms.ModelForm):
    class Meta:
        model = ScoreDetail
        fields = [
            'credit', 's_check', 's_test', 's_homework', 
            's_activity', 's_project', 's_midterm', 's_final', 'ps'
        ]  # Update with the desired fields from your UserProfile model
