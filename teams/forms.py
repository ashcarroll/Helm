from django import forms
from django.contrib.auth.models import User
from .models import Team

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
        required = False
    )

    class Meta:
        model = Team
        fields = ['name', 'members']