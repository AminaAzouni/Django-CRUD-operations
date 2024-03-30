from django import forms 
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User 
from .models import Student  

class SignupForm(UserCreationForm):
      class Meta:
            model= User
            # fields will be include in the forms
            fields= ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
      username=forms.CharField(widget=forms.TextInput())
      password=forms.CharField(widget=forms.PasswordInput())
      
class StudentForm(forms.ModelForm):
      class Meta:
            model= Student
            fields= ['name', 'email', 'age', 'gender']

