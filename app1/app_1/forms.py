from django.forms import CharField, ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Document,Role,Student_Document

class UploadForm(ModelForm):
    class Meta:
        model = Document
        fields = ['title','author']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password','first_name','last_name','role']
        widgets = {'password': forms.PasswordInput()}
    