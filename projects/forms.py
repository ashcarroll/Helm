from django import forms
from django.contrib.auth.models import User
from .models import Project, Task

class ProjectForm(forms.ModelForm):
    project_team = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = False
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'start_date', 'end_date', 'project_team']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date']