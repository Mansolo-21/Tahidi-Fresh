from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=40,
                               widget=forms.TextInput(
                                   attrs={
                                       "class":"form-control",
                                       "placeholder":"Username"
                                   }
                               ))
    email = forms.EmailField(widget=forms.EmailInput(
                                   attrs={
                                       "class":"form-control",
                                       "placeholder":"Email Address"
                                   }
                               ))
    password1 = forms.CharField(widget=forms.PasswordInput(
                                   attrs={
                                       "class":"form-control",
                                       "placeholder":"Password"
                                   }
                               ))
    password2 = forms.CharField(widget=forms.PasswordInput(
                                   attrs={
                                       "class":"form-control",
                                       "placeholder":"Confirm Password"
                                   }
                               ))
    phone_number=forms.CharField(max_length=30,required=False,
                                   widget=forms.TextInput(
                                       attrs={
                                           "class":"form-control",
                                           "placeholder":"Phone Number"
                                       }
                                   ))
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return 
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    "Passwords don't match."
                )
            validate_password(password1)
        return cleaned_data
    
class LoginForm(forms.Form):
    username =forms.CharField(max_length=40,
                              widget=forms.TextInput(
                                  attrs={
                                      "class":"form-control",
                                      "placeholder":"Username"
                                  }
                              ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                    "class":"form-control",
                    "placeholder":"Password"
            }
        )
    )