from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))
    
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name","email","password",'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'form3Example1c'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'form3Example1c'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'form3Example1c'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'form3Example1c'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'form3Example1c'}),
        }