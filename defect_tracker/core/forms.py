# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Project, Defect, UserProfile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ['title', 'description', 'assigned_to', 'status']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['qualifications', 'skills', 'bio']