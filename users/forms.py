from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('IC', 'IC'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Role')
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']