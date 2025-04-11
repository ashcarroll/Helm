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

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if project:
            # Only have choics for assigned_to show for project team members
            self.fields['assigned_to'].queryset = project.project_team.all()