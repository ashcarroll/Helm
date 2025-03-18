from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from .models import Project
from .forms import ProjectForm

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create_project.html'

    def form_valid(self, form):
        project = form.save(commit=False)
        project.manager = self.request.user
        project.save()
        messages.success(self.request, "Project has been created successfully")

        return redirect('project_list')
    
    def test_func(self):
        # Only managers can access this view
        return self.request.user.groups.filter(name='Manager').exists()
    
    def handle_no_permission(self):
        # Error handling to protect view on the backend, incase URL is guessed and UI constraints are bypassed
        messages.error(self.request, "Only managers can create projects")
        return redirect('project_list')