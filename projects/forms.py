from django import forms
from django.contrib.auth.models import User
from .models import Project

class ProjectForm(forms.ModelForm):
    project_team = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = False
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'start_date', 'end_date', 'project_team']